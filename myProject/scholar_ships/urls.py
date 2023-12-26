from django.urls import path 
from . import views
urlpatterns = [
    path('add_view/scholarship/', views.add_view_scholarship),
    path('provider_scholarship/', views.provider_scholarship),
    path('delete_update/scholarship/<int:pk>/', views.delete_update_scholarship),
    path('favlist/', views.FavList),
    path('add/fav/<int:pk>/', views.Add_Fav),
]