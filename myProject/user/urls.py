from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register),
    path('login/provider/', views.login_provider),
    path('login/seeker/', views.login_seeker),
    path('activate/<str:uidb64>/<str:token>/', views.activate_Email, name='activate'),
    path('resend_email/', views.re_send_email_verification),
    path('reset_password/', views.reset_password),
    path('reset/<str:uidb64>/<str:token>/',views.Reset_Password)
    
]