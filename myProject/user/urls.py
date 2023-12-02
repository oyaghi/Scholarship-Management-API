from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register),
    path('get/', views.Get),
    path('login/provider/', views.login_provider),
]