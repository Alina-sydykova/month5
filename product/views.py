from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import (
    ReviewSerializer,
    ProductSerializer,
    ProductWithReviewsSerializer,
    CategoryWithCountSerializer
)



@api_view(['GET', 'POST'])
def category_list_create_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = CategoryWithCountSerializer(categories, many=True).data
        return Response(data=data)
    
    elif request.method == 'POST':
        serializer = CategoryWithCountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_update_delete_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)

    if request.method == 'GET':
        data = CategoryWithCountSerializer(category).data
        return Response(data=data)
    
    elif request.method == 'PUT':
        serializer = CategoryWithCountSerializer(instance=category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=204)




@api_view(['GET', 'POST'])
def product_list_create_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data=data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_update_delete_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

    if request.method == 'GET':
        data = ProductSerializer(product).data
        return Response(data=data)
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=204)


@api_view(['GET'])
def product_with_reviews_view(request):
    products = Product.objects.all()
    data = ProductWithReviewsSerializer(products, many=True).data
    return Response(data=data)




@api_view(['GET', 'POST'])
def review_list_create_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_update_delete_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=404)

    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data=data)
    
    elif request.method == 'PUT':
        serializer = ReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=204)
