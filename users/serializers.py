from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()

# ========================================
# UTILITY FUNCTION
# ========================================
def validate_password_strength(value):
    """
    Valide le mot de passe contre les règles Django (AUTH_PASSWORD_VALIDATORS).
    Wrapper qui formatte les erreurs pour l'API REST.

    Utilisée dans tous les serializers qui demandent un password.
    """
    try:
        validate_password(value)
    except DjangoValidationError as e:
        raise ValidationError({
            "error_code": "WEAK_PASSWORD",
            "details": e.messages
        })

# ========================================
# USER SERIALIZER (Read-only)
# ========================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
        read_only_fields = ['id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Appel de la méthode parente pour obtenir le token de base
        token = super().get_token(user)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_staff'] = user.is_staff

        return token

# ========================================
# SIGN IN ET SIGN UP SERIALIZERS
# ========================================
class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        # 1. Vérifier que l'email n'existe pas
        if User.objects.filter(email=email).exists():
            raise ValidationError({
            "error_code": "EMAIL_ALREADY_EXISTS",
            "message": "Cet email existe déjà"
        })

        # 2. Vérifier que les mots de passe correspondent
        if password != password_confirm:
            raise ValidationError({
            "error_code": "PASSWORD_MISMATCH",
            "message": "Les mots de passe ne correspondent pas"
        })

        # 3. Valider la force du mot de passe
        validate_password_strength(password)

        return data

    def create(self, validated_data):

        validated_data.pop('password_confirm')

        return User.objects.create_user(**validated_data)

# ========================================
# PASSWORD RESET SERIALIZERS
# ========================================
class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Valide que l'email est fourni et au bon format.
    """
    email = serializers.EmailField(required=True)

class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Valide les 3 éléments nécessaires pour confirmer la réinitialisation :
    - uidb64 : l'ID utilisateur encodé en base64
    - token : le token de réinitialisation signé
    - password : le nouveau mot de passe
    """
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        """Valide le nouveau mot de passe"""
        validate_password_strength(value)
        return value
