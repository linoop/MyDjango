from unicodedata import name
from django.urls import path
from myapp.api import views


urlpatterns = [
    path('', views.getRoutes),
    path('product/', views.ProductManager.as_view(), name='product'),
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('signup/', views.createUser)
]