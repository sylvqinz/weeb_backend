from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import CustomTokenObtainPairView, RegisterView

urlpatterns = [
    # Sign Up
    path('register/', RegisterView.as_view(), name='register'),

    # Sign In
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),

    # Refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]