from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    
    # Category URL's
    
    path('add_category/', views.add_category, name='add_category'),
    path('view_category/', views.view_category, name='view_category'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('update_category/<int:pk>/', views.update_category, name='update_category'),
    
    # Subcategory URL's
    
    path('add_subcategory', views.add_subcategory, name="add_subcategory"),
    path('view_subcategory', views.view_subcategory, name="view_subcategory"),
    path('delete_subcategory/<int:pk>/', views.delete_subcategory, name="delete_subcategory"),
    path('update_subcategory/<int:pk>/', views.update_subcategory, name="update_subcategory"),
    

    # Transaction URL's

    path('add_products', views.add_products, name="add_products"),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
    path('add_row/', views.add_row, name='add_row'),
    path('view_products/', views.view_products, name='view_products'),
    path('make_transaction/<int:pk>', views.make_transaction, name='make_transaction'),
 
]

