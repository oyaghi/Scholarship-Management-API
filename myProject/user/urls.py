from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register),
    path('login/provider/', views.login_provider),
    path('login/seeker/', views.login_seeker),
    path('get/provdier/', views.view_provider),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate)
]