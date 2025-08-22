
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
import random

from users.models import ConfirmationCode


@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return Response({"error": "Все поля обязательны."}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Пользователь уже существует."}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    user.is_active = False
    user.save()

    code = random.randint(100000, 999999)
    ConfirmationCode.objects.create(user=user, code=code)

    return Response({"message": "Пользователь создан. Подтвердите код.", "code": code})


@api_view(['POST'])
def confirm_view(request):
    username = request.data.get('username')
    code = request.data.get('code')

    try:
        user = User.objects.get(username=username)
        confirm = ConfirmationCode.objects.get(user=user)

        if str(confirm.code) == str(code):
            user.is_active = True
            user.save()
            confirm.delete()
            return Response({"message": "Пользователь подтвержден!"})
        else:
            return Response({"error": "Неверный код."}, status=400)

    except User.DoesNotExist:
        return Response({"error": "Пользователь не найден."}, status=404)
    except ConfirmationCode.DoesNotExist:
        return Response({"error": "Код подтверждения не найден."}, status=404)
