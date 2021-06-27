from django.contrib import admin
from django.urls import path
from . import views
app_name='account'
urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('registraiton/',views.user_register,name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('dashbord/<int:user_id>/', views.user_dashboard, name='dashboard'),
    path('edit_profile/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('follow/',views.follow,name='follow '),
    path('unfollow/',views.unfollow,name='unfollow '),
]