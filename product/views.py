from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Category, Product, Review
from .serializers import (
    ReviewSerializer,
    ProductSerializer,
    ProductWithReviewsSerializer,
    CategoryWithCountSerializer,
    RegisterSerializer,
    ConfirmSerializer
)





class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Регистрация прошла успешно. Проверьте код."}, status=201)
        return Response(serializer.errors, status=400)


class ConfirmView(APIView):
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь успешно активирован"})
        return Response(serializer.errors, status=400)




class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithCountSerializer


class CategoryDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithCountSerializer
    lookup_field = 'id'

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class ProductWithReviewsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductWithReviewsSerializer(products, many=True)
        return Response(serializer.data)





class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'
