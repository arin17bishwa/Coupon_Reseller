from django.urls import path

from .views import (
    home_view,
    welcome_view,
    homeView,
)

app_name='personal'

urlpatterns = [
    path('',home_view,name='home'),
    path('welcome/',welcome_view,name='welcome'),
    path('home/',homeView,name='Home')
]
