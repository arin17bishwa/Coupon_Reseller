from django.urls import path

from .views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    must_authenticate_view,
    activate,
    profile_view,
    create_profile_view,
)

app_name='account'

urlpatterns = [
    path('account/',account_view,name='profile'),
    path('login/',login_view,name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'),
    path('must-authenticate/', must_authenticate_view, name='must_authenticate'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('profile/<slug>/',profile_view,name='profileData_view'),
    path('profile/create/<slug>',create_profile_view,name='create_profile')
]
