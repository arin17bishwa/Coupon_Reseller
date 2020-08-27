from django.urls import path

from .views import (
    home_view,
    welcome_view,
)

app_name='personal'

urlpatterns = [
    path('',home_view,name='home'),
    path('welcome/',welcome_view,name='welcome'),
]
