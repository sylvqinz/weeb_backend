from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    """
    Vue personnalisée pour l'obtention de token qui utilise notre serializer personnalisé
    pour inclure des informations supplémentaires dans le token.
    """
    serializer_class = MyTokenObtainPairSerializer
