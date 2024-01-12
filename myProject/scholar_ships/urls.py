from django.urls import path 
from . import views
urlpatterns = [
    path('add_view/scholarship/', views.AddViewScholarship.as_view()),
    path('provider_scholarship/', views.ProviderScholarships.as_view(),),
    path('delete_update/scholarship/<int:pk>/', views.DeleteUpdateScholarships.as_view()),
    path('favlist/', views.Favorite.as_view()),
    path('add/fav/<int:pk>/', views.Favorite.as_view()),
]