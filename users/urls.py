from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('', index, name='index'),
    path('register/',signup, name='signup'),
    path('login/',login,name='login'),
    path('logout/',custom_logout,name='logout'),
    path('activate/<uidb64>/<token>',activate,name='activate'),
    path('password-reset/',CustomPasswordResetView,name='password_reset'),
    path('reset/<uidb64>/<token>/',CustomPasswordResetConfirmView,name='password_reset_confirm'),
]