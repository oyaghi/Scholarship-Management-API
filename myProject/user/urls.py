from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.Register.as_view()),
    path('login/provider/', views.LoginProvider.as_view()),
    path('login/seeker/', views.LoginSeeker.as_view()),
    path('activate/<str:uidb64>/<str:token>/', views.ActivateEmail.as_view(), name='activate'),
    path('resend_email/', views.ReSendEmailVerification.as_view()),
    path('reset_password/', views.ResetPassword.as_view()),
    path('reset/<str:uidb64>/<str:token>/',views.ResetPasswordConfirm.as_view()),
    
]