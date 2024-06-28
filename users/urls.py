from django.urls import path
from .views import *

urlpatterns=[
    path('', index, name='index'),
    path('register/',signup, name='signup'),
    path('login/',login,name='login'),
    path('logout/',custom_logout,name='logout'),
    path('activate/<uidb64>/<token>',activate,name='activate'),
]