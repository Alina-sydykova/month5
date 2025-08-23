
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User  
from users.services import (
    generate_confirmation_code,
    get_confirmation_code,
    delete_confirmation_code,
)


class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "birthday"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()

        
        generate_confirmation_code(user.email)

        
        return user


class LoginSerializer(serializers.Serializer):
  
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Должны быть предоставлены email и пароль")

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Неверный email или пароль")
        if not user.is_active:
            raise serializers.ValidationError("Аккаунт не подтверждён")

        data["user"] = user
        return data

class ConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        
        email = data["email"].strip().lower()
        input_code = data["code"].strip()

        stored_code = get_confirmation_code(email)
        if not stored_code or stored_code != input_code:
            raise serializers.ValidationError("Неверный email или код подтверждения")
       
        data["email"] = email
        data["code"] = input_code
        return data

    def save(self):
       
        user = User.objects.get(email=self.validated_data["email"])
        user.is_active = True
        user.save()
        delete_confirmation_code(user.email)
