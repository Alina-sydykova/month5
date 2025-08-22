
import os
import requests
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

GOOGLE_TOKENINFO = "https://oauth2.googleapis.com/tokeninfo"
GOOGLE_USERINFO  = "https://www.googleapis.com/oauth2/v3/userinfo"
GOOGLE_TOKEN     = "https://oauth2.googleapis.com/token"


def exchange_code_for_token(code: str):
    """Меняем authorization code на access_token Google."""
    data = {
        "code": code,
        "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
        "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI"),
        "grant_type": "authorization_code",
    }
    r = requests.post(GOOGLE_TOKEN, data=data, timeout=15)
    try:
        r.raise_for_status()
        return r.json(), None
    except requests.HTTPError:
        return None, r.json()


def userinfo_by_access_token(access_token: str):
    """Получаем email/given_name/family_name пользователя у Google по access_token."""
    r = requests.get(
        GOOGLE_USERINFO,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    try:
        r.raise_for_status()
        return r.json(), None
    except requests.HTTPError:
        return None, r.json()


def verify_id_token(id_token: str, client_id: str):
    """Быстрая валидация id_token через tokeninfo (для локальной отладки ок)."""
    r = requests.get(GOOGLE_TOKENINFO, params={"id_token": id_token}, timeout=15)
    try:
        r.raise_for_status()
    except requests.HTTPError:
        return None, r.json()
    payload = r.json()
    if payload.get("aud") != client_id:
        return None, {"error": "invalid_audience", "expected": client_id, "got": payload.get("aud")}
    return payload, None


class GoogleLoginAPIView(APIView):
    

    def get(self, request):
        code = request.query_params.get("code")
        if not code:
            return Response({"detail": "Нет ?code=... в query"}, status=400)
        return self._handle_via_code(code)

    def post(self, request):
        code = request.data.get("code")
        id_token = request.data.get("id_token")
        access_token = request.data.get("access_token")

        if code:
            return self._handle_via_code(code)
        if id_token:
            return self._handle_via_id_token(id_token)
        if access_token:
            return self._handle_via_access_token(access_token)

        return Response({"detail": "Нужен 'code' ИЛИ 'id_token' ИЛИ 'access_token'."}, status=400)

    # --- Ветки обработки ---

    def _handle_via_code(self, code: str):
        token_data, token_err = exchange_code_for_token(code)
        if not token_data or not token_data.get("access_token"):
            # Диагностика: видно, что реально подставилось из .env
            return Response({
                "error": "Не удалось обменять code на access_token",
                "details": token_err,
                "diag": {
                    "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                    "redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI"),
                    "has_secret": bool(os.environ.get("GOOGLE_CLIENT_SECRET")),
                }
            }, status=400)
        return self._issue_local_jwt(token_data["access_token"])

    def _handle_via_access_token(self, access_token: str):
        return self._issue_local_jwt(access_token)

    def _handle_via_id_token(self, id_token: str):
        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        payload, err = verify_id_token(id_token, client_id)
        if not payload or not payload.get("email"):
            return Response({"error": "Не удалось верифицировать id_token", "details": err}, status=400)

        email = payload.get("email")
        given_name = payload.get("given_name")
        family_name = payload.get("family_name")

        user, created = User.objects.get_or_create(email=email)
        if created or not user.first_name or not user.last_name:
            if given_name:
                user.first_name = given_name
            if family_name:
                user.last_name = family_name
        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email
        if getattr(user, "birthday", None):
            refresh["birthday"] = user.birthday.isoformat()

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {"email": user.email, "first_name": user.first_name, "last_name": user.last_name}
        }, status=200)

  
    def _issue_local_jwt(self, access_token: str):
        ui, err = userinfo_by_access_token(access_token)
        if not ui or not ui.get("email"):
            return Response({"error": "Не удалось получить userinfo", "details": err}, status=400)

        email = ui.get("email")
        given_name = ui.get("given_name")
        family_name = ui.get("family_name")

        user, created = User.objects.get_or_create(email=email)
        if created or not user.first_name or not user.last_name:
            if given_name:
                user.first_name = given_name
            if family_name:
                user.last_name = family_name
        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email
        if getattr(user, "birthday", None):
            refresh["birthday"] = user.birthday.isoformat()

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {"email": user.email, "first_name": user.first_name, "last_name": user.last_name}
        }, status=200)
