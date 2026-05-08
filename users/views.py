from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vue personnalisée pour l'obtention de token qui utilise notre serializer personnalisé
    pour inclure des informations supplémentaires dans le token.
    """
    serializer_class = CustomTokenObtainPairSerializer
