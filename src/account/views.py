from operator import attrgetter

from coupons.models import Coupon
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import (
    RegistrationForm,
    AccountAuthenticationForm,
    AccountUpdateForm,
    UserProfileForm,
    ProfileUpdateForm,
)
from .models import User, UserProfile
from .utils import account_activation_token


import sqlite3

# Create your views here.

HALLS=settings.HALLS
User=get_user_model()


# Create your views here.

def registration_view(request):
    context={}
    if request.POST:
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.registration_no=str(user.registration_no).upper()
            conn = sqlite3.connect('account/bt_all.sqlite3')
            cur = conn.cursor()
            cur.execute('SELECT name FROM BTECH_all WHERE reg= ? ', (user.registration_no.upper(),))
            name = cur.fetchone()
            if name is not None:
                name = name[0]
                name_verified = True
            else:
                name_verified = False
            #print(name, name_verified)
            user.name_verified=name_verified
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your Coupon_Reseller account.'
            message = render_to_string('account/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            #email.send()
            print(message)
            return HttpResponse('Please confirm your email address to complete the registration')

        else:
            context['registration_form']=form
    else:#it means it is a GET request
        form=RegistrationForm()
        context['registration_form'] = form
    return render(request,'account/register.html',context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:create_profile',slug=str(user.registration_no).lower())
    else:
        return HttpResponse('Activation link is invalid!')

def logout_view(request):
    logout(request)
    return redirect('personal:home')

def login_view(request):
    context={}

    user=request.user
    if user.is_authenticated:
        return redirect('personal:home')

    if request.POST:
        form=AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)

            if user:
                if not user.is_active:return HttpResponse('YOUR ACCOUNT IS NOT ACTIVE YET')
                login(request,user)
                return redirect('personal:home')
    else:
        form=AccountAuthenticationForm()

    context['login_form']=form
    return render(request,'account/login.html',context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect('account:must_authenticate')

    context={}

    if request.POST:
        form=AccountUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.initial={
                'username':request.POST['username']
            }
            form.save()
            context['success_message']='Account Updated Successfully!'
    else:
        form=AccountUpdateForm(
            initial={
                'username':request.user.username,
            }
        )
    context['account_form']=form
    qs=Coupon.objects.filter(author=request.user)
    context['coupon_posts']=sorted(list(qs),key=attrgetter('date_updated'),reverse=True)
    return render(request,'account/account.html',context)

def must_authenticate_view(request):
    return render(request,'account/must_authenticate.html')

def profile_view(request,slug):
    context={}
    context['has_profile']=False
    user=request.user
    if not request.user.is_authenticated:
        return redirect('account:must_authenticate')

    if (not hasattr(user,'userprofile')) or str(user.userprofile.name).strip()=='':
        return redirect('account:create_profile',slug=str(user.registration_no.lower()))

    profile=get_object_or_404(UserProfile,slug=slug.lower())
    context['profile'] = profile
    if profile.user!=user:
        return render(request,'account/view_profile.html',context)

    if request.POST:
        form=ProfileUpdateForm(request.POST or None,instance=request.user.userprofile)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.hall=int(request.POST.get('hall'))

            if user.name_verified:
                conn = sqlite3.connect('account/bt_all.sqlite3')
                cur = conn.cursor()
                cur.execute('SELECT name FROM BTECH_all WHERE reg= ? ', (user.registration_no.upper(),))
                name = cur.fetchone()[0]
                obj.name=name

            obj.save()
            profile=obj
            context['success_message']='Account Updated Successfully!'

    form=ProfileUpdateForm(
        initial={
            'name':profile.name,
            'hall':profile.hall,
            #'veg':profile.veg
        }
    )

    context['profile_form']=form

    return render(request,'account/edit_profile.html',context)


def create_profile_view(request,slug):
    context={}
    user=request.user
    if (not request.user.is_authenticated):
        return redirect('account:must_authenticate')
    if user.registration_no.lower()!=slug:
        return redirect('account:must_authenticate')

    account=get_object_or_404(User,registration_no=slug.upper())#######

    if not account:return HttpResponse('Sorry, But no such account was found.....\nAnd please stop messing around with the system....')
    #context['HALLS']=HALLS


    if request.POST:
        form=UserProfileForm(request.POST)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.hall=int(request.POST.get('hall'))
            owner=User.objects.filter(registration_no=user.registration_no.upper()).first()
            profile.user=owner
            if user.name_verified:
                conn = sqlite3.connect('account/bt_all.sqlite3')
                cur = conn.cursor()
                cur.execute('SELECT name FROM BTECH_all WHERE reg= ? ', (user.registration_no.upper(),))
                name = cur.fetchone()[0]
                profile.name=name

            profile.save()
            return redirect('personal:home')
        else:
            context['form']=form
    else:
        form=UserProfileForm()
        context['form']=form
    
    return render(request,'account/create_profile.html',context=context)