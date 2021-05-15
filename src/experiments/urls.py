from django.urls import path
from . import views

app_name='account'

urlpatterns = [
    path('pin/<int:pin>/',views.pin_api,name='pin'),
]
