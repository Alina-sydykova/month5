from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from .models import Category, Product, Review
from .serializers import (
    ReviewSerializer,
    ProductSerializer,
    ProductWithReviewsSerializer,
    CategoryWithCountSerializer,
)
from users.serializers import RegisterSerializer, ConfirmSerializer, LoginSerializer
from common.permissions import IsModerator
from common.validators import validate_age_18
from users.serializers import RegisterSerializer, ConfirmSerializer, LoginSerializer

from django.core.exceptions import ValidationError


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Регистрация прошла успешно. Проверьте код."}, status=status.HTTP_201_CREATED)


class ConfirmView(APIView):
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь успешно активирован"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


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

    def get_permissions(self):
        from rest_framework.permissions import IsAuthenticated
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return []

    def create(self, request, *args, **kwargs):
        
        payload = getattr(request, "auth", {}) or {}
        birthday = payload.get("birthday") if hasattr(payload, "get") else None

        try:
            validate_age_18(birthday)
        except ValidationError as e:
            
            return Response({"detail": "Вам должно быть 18 лет, чтобы создать продукт."},
                            status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)



class ProductDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    permission_classes = [IsModerator] 

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
