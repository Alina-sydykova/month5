from django.urls import path
from . import views

urlpatterns = [
    
    path('categories/', views.category_list_create_view),
    path('categories/<int:id>/', views.category_detail_update_delete_view),

   
    path('products/', views.product_list_create_view),
    path('products/<int:id>/', views.product_detail_update_delete_view),
    path('products/reviews/', views.product_with_reviews_view),

    
    path('reviews/', views.review_list_create_view),
    path('reviews/<int:id>/', views.review_detail_update_delete_view),


    path('auth/register/', views.register_view),
    path('auth/confirm/', views.confirm_view),
]

