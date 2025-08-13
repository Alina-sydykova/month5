from rest_framework import serializers
from .models import Category, Product, Review, User, ConfirmationCode



from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'last_name', 'phone_number']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError("Неверный email или пароль")
        else:
            raise serializers.ValidationError("Должны быть предоставлены email и пароль")

        data['user'] = user
        return data



class ConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            confirm = ConfirmationCode.objects.get(user=user, code=data['code'])
        except (User.DoesNotExist, ConfirmationCode.DoesNotExist):
            raise serializers.ValidationError("Неверный email или код подтверждения")
        return data

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.is_active = True
        user.is_verified = True
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
        if reviews.exists():
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
