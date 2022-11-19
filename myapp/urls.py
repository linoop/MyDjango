from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUserPage, name='login'),
    path('register/', views.registerUserPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.homePage, name='home'),
    path('profile/<str:pk>', views.userProfile, name='user_profile'),
    path('topics/', views.topicPage, name='topics'),
    path('create-room/', views.createRoom, name='create_room'),
]