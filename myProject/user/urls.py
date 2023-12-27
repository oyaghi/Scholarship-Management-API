from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register),
    path('login/provider/', views.login_provider),
    path('login/seeker/', views.login_seeker),
    path('get/provdier/', views.view_provider),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate')
]