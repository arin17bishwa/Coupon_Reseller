from operator import attrgetter
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from coupons.models import Coupon
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

POSTS_PER_PAGE = settings.POSTS_PER_PAGE


# Create your views here.

def home_view(request):
    context = {}
    if not request.user.is_authenticated: return redirect('account:must_authenticate')
    qs_coupons = Coupon.objects.all()
    # qs=Coupon.objects.filter(date_updated__gte=(timezone.now()-timedelta(hours=36)))
    qs = qs_coupons.filter(sold=False).exclude(author=request.user)
    if request.GET:
        filter_data = request.GET
        f_hall = filter_data.get('hall', 'None')
        f_hall = None if (not str(f_hall).isdecimal()) else int(f_hall)

        f_meal = filter_data.get('meal', 'None')
        f_meal = None if (f_meal == 'None') else f_meal

        if f_hall: qs = qs.filter(hall=f_hall)
        if f_meal: qs = qs.filter(meal=f_meal)

    posts = sorted(list(qs), key=attrgetter('date_updated'), reverse=True)
    posts.sort(key=attrgetter('price'))

    # PAGINATION
    page = request.GET.get('page', 1)
    posts_paginator = Paginator(posts, POSTS_PER_PAGE)
    try:
        posts = posts_paginator.page(page)
    except PageNotAnInteger:
        posts = posts_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        posts = posts_paginator.page(posts_paginator.num_pages)

    context['coupon_posts'] = posts
    return render(request, 'personal/home.html', context=context)


def welcome_view(request):
    context = {'message': 'WELCOME EVERYONE'}
    return render(request, 'personal/home.html', context=context)
