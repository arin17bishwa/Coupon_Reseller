from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view

from .forms import (CreateCouponForm, UpdateCouponForm)
# Create your views here.
from .models import Coupon

User=get_user_model()
HALLS=settings.HALLS
MEALS=settings.MEALS
def create_coupon_view(request):
    context={}

    user=request.user
    if not user.is_authenticated:
        return redirect('account:must_authenticate')

    if (not hasattr(user,'userprofile')) or user.userprofile.name=='':
        return redirect('account:create_profile',slug=str(user.registration_no).lower())

    form=CreateCouponForm(request.POST or None)
    if form.is_valid():
        obj=form.save(commit=False)
        author=User.objects.filter(email=user.email).first()
        obj.author=author
        obj.save()
        form=CreateCouponForm()
    context['form']=form
    return render(request,'coupons/create_post.html',context)


def update_coupon_view(request,slug):
    context={}
    context['HALLS']=HALLS
    context['MEALS']=MEALS
    user=request.user
    if not user.is_authenticated:return redirect('account:must_authenticate')
    post=get_object_or_404(Coupon,slug=slug)
    if post.author!=user: return redirect('account:must_authenticate')
    if request.POST:
        form=UpdateCouponForm(request.POST or None,instance=post)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.sold=int(request.POST['sold'])
            obj.save()
            post=obj

            context['success_message']='Updated'

    form = UpdateCouponForm(
        initial={
            'meal': post.meal,
            'hall': post.hall,
            'price': post.price,
            'sold':post.sold
        }
    )

    context['form'] = form
    return render(request,'coupons/update_post.html',context=context)

@api_view(['POST'])
def coupon_action_view(request):
    if request.is_ajax():
        data=request.data
        coupon=get_object_or_404(Coupon,slug=data.get('slug'))
        if data['action']=='yes':
            coupon.sold=True
            coupon.save()
    return redirect('account:profile')