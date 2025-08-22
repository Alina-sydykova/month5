from django.urls import path
from users.oauth import GoogleLoginAPIView

urlpatterns = [
    
    path("api/v1/auth/google/", GoogleLoginAPIView.as_view(), name="google-login"),
]
