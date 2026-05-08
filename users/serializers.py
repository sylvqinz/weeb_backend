from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
        read_only_fields = ['id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']

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

        if User.objects.filter(email=email).exists():
            raise ValidationError({
            "error_code": "EMAIL_ALREADY_EXISTS",
            "message": "Cet email existe déjà"
        })

        if password != password_confirm:
            raise ValidationError({
            "error_code": "PASSWORD_MISMATCH",
            "message": "Les mots de passe ne correspondent pas"
        })

        try :
            validate_password(password)
        except DjangoValidationError as e:
            raise ValidationError({
            "error_code": "WEAK_PASSWORD",
            "details": e.messages
        })

        return data

    def create(self, validated_data):

        password = validated_data.pop('password')
        validated_data.pop('password_confirm')

        user = User.objects.create_user(password = password, **validated_data)

        token = CustomTokenObtainPairSerializer.get_token(user)

        return {
            "message": "Utilisateur créé avec succès",
            "user": UserSerializer(user).data,
            "tokens": {
                "access": str(token.access_token),
                "refresh": str(token)
            }
        }