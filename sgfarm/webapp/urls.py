from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('add_category/', views.add_category, name='add_category'),
    path('view_category/', views.view_category, name='view_category'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('update_category/<int:pk>/', views.update_category, name='update_category'),
    
 
]
