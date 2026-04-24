from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Appel de la méthode parente pour obtenir le token de base
        token = super().get_token(user)

        token['first_name'] = user.first_name
        token['last_name'] = user.last_name


        return token