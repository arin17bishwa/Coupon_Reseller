from operator import attrgetter

# Create your views here.
from coupons.models import Coupon
from django.shortcuts import render, redirect


def home_view(request):
    if not request.user.is_authenticated:return redirect('account:must_authenticate')
    context={}
    qs = Coupon.objects.filter(sold=False).exclude(author=request.user)
    posts=sorted(list(qs),key=attrgetter('date_updated'),reverse=True)
    context['coupon_posts'] = posts
    context['message'] = 'HELLO EVERYONE'
    return render(request, 'personal/home.html', context=context)

def welcome_view(request):
    context = {}
    context['message'] = 'WELCOME EVERYONE'
    return render(request, 'personal/home.html', context=context)

def homeView(request):
    pass