from rest_framework import serializers
from .models import Category, Product, Review

from django.contrib.auth.models import User
from .models import ConfirmationCode


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            is_active=False
        )
        ConfirmationCode.objects.create(user=user)  
        print(f"Confirmation code for {user.username}: {user.confirmationcode.code}")  
        return user


class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
            confirm = ConfirmationCode.objects.get(user=user, code=data['code'])
        except (User.DoesNotExist, ConfirmationCode.DoesNotExist):
            raise serializers.ValidationError("Неверное имя пользователя или код")
        return data

    def save(self):
        user = User.objects.get(username=self.validated_data['username'])
        user.is_active = True
        user.save()
        ConfirmationCode.objects.filter(user=user).delete()



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Название категории слишком короткое.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_title(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Название продукта слишком короткое.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_stars(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Оценка (stars) должна быть от 1 до 5.")
        return value

    def validate_text(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Текст отзыва не может быть пустым.")
        return value


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'reviews', 'average_rating']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            total = sum([review.stars for review in reviews])
            return round(total / len(reviews), 1)
        return None


class CategoryWithCountSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.products.count()
