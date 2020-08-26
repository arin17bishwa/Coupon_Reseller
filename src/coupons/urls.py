from django.urls import path

from .views import (
    create_coupon_view,
    update_coupon_view,
    coupon_action_view,
)

app_name='coupons'

urlpatterns = [
    path('create/',create_coupon_view,name='create'),
    path('update/<slug>/',update_coupon_view,name='update'),
    path('action/',coupon_action_view,name='actions')
]
