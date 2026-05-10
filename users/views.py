from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserRegisterSerializer, UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vue personnalisée pour l'obtention de token qui utilise notre serializer personnalisé
    pour inclure des informations supplémentaires dans le token.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh_token = response.data.get("refresh")
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="Strict",
                max_age=7 * 24 * 60 * 60
            )
            del response.data["refresh"]
            response.data["message"] = "Connexion réussie"

        return response


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Sérialiseur crée l'user
        user = serializer.save()

        # Vue gère les tokens et cookies
        token = CustomTokenObtainPairSerializer.get_token(user)

        response = Response({
            "message": "Utilisateur créé avec succès",
            "user": UserSerializer(user).data,
            "tokens": {"access": str(token.access_token)}
        }, status=status.HTTP_201_CREATED)

        response.set_cookie(
            key="refresh_token",
            value=str(token),
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=7 * 24 * 60 * 60
        )

        return response