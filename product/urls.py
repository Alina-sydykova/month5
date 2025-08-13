from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailUpdateDeleteView,
    ProductListCreateView, ProductDetailUpdateDeleteView,
    ProductWithReviewsView,
    ReviewListCreateView, ReviewDetailUpdateDeleteView
)
from . import auth_views

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view()),
    path('categories/<int:id>/', CategoryDetailUpdateDeleteView.as_view()),

    path('products/', ProductListCreateView.as_view()),
    path('products/<int:id>/', ProductDetailUpdateDeleteView.as_view()),
    path('products/reviews/', ProductWithReviewsView.as_view()),

    path('reviews/', ReviewListCreateView.as_view()),
    path('reviews/<int:id>/', ReviewDetailUpdateDeleteView.as_view()),

    path('register/', auth_views.register_view),
    path('confirm/', auth_views.confirm_view),
]

 


from rest_framework_simplejwt.views import TokenObtainPairView
from .tokens import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
