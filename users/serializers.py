
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, ConfirmationCode


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'birthday']

    def create(self, validated_data):
        
        user = User.objects.create_user(**validated_data)
        
        user.is_active = False
        user.save()
        ConfirmationCode.objects.update_or_create(user=user, defaults={})
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
            ConfirmationCode.objects.get(user=user, code=data['code'])
        except (User.DoesNotExist, ConfirmationCode.DoesNotExist):
            raise serializers.ValidationError("Неверный email или код подтверждения")
        return data

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.is_active = True
        user.save()
      
        ConfirmationCode.objects.filter(user=user).delete()
