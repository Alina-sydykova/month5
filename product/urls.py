
from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailUpdateDeleteView,
    ProductListCreateView, ProductDetailUpdateDeleteView,
    ProductWithReviewsView,
    ReviewListCreateView, ReviewDetailUpdateDeleteView,
    RegisterView, ConfirmView, LoginView,
)

urlpatterns = [
    
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm/', ConfirmView.as_view(), name='confirm'),
    path('login/', LoginView.as_view(), name='login'),  

    path('categories/', CategoryListCreateView.as_view(), name='categories'),
    path('categories/<int:id>/', CategoryDetailUpdateDeleteView.as_view(), name='category_detail'),

    
    path('products/', ProductListCreateView.as_view(), name='products'),
    path('products/<int:id>/', ProductDetailUpdateDeleteView.as_view(), name='product_detail'),
    path('products/reviews/', ProductWithReviewsView.as_view(), name='products_with_reviews'),

    
    path('reviews/', ReviewListCreateView.as_view(), name='reviews'),
    path('reviews/<int:id>/', ReviewDetailUpdateDeleteView.as_view(), name='review_detail'),
]


