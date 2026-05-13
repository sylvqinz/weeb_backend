from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserRegisterSerializer, UserSerializer, \
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer

User = get_user_model()
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
            access_token = response.data.get("access")
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="Strict",
                max_age=7 * 24 * 60 * 60
            )
            response.data = {
                "message": "Connexion réussie",
                "access": access_token,
                "user": UserSerializer(request.user).data  # ← Ici !
            }

        return response


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # créer l'user
        user = serializer.save()

        # Vue gère les tokens et cookies
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({
            "message": "Utilisateur créé avec succès",
            "user": UserSerializer(user).data,
            "access": access_token
        }, status=status.HTTP_201_CREATED)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=7 * 24 * 60 * 60
        )

        return response


class RequestPasswordResetEmailView(generics.GenericAPIView):
    """
    Première étape du reset password : l'utilisateur envoie son email.

    POST /users/password-reset/request/
    Body: {"email": "user@example.com"}
    """
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        # Cherche l'utilisateur (silencieusement, sans révéler son existence)
        user = User.objects.filter(email=email).first()

        if user:
            # Génère les éléments du lien de réinitialisation
            # Encoder l'ID de l'utilisateur en base64 (rend l'ID "URL-safe")
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            # Générer le token cryptographique
            token = PasswordResetTokenGenerator().make_token(user)

            # Construit l'URL complète pour React
            frontend_url = settings.FRONTEND_URL
            reset_url = f"{frontend_url}/reset-password?uidb64={uidb64}&token={token}"

            # TODO: Envoyer l'email réel ici avec le lien
            # Pour l'instant, affiche dans la console pour les tests
            print(f"\n--- EMAIL DE RÉINITIALISATION ENVOYÉ À {user.email} ---")
            print(f"Lien de réinitialisation : {reset_url}")
            print("-------------------------------------------------------\n")

        # Réponse générique TOUJOURS, peu importe si l'email existe ou non
        # Cela empêche l'énumération d'utilisateurs (user enumeration attack)
        return Response(
            {
                "message": "Si un compte est associé à cet email, vous recevrez des instructions pour réinitialiser votre mot de passe."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    Deuxième étape du reset password : l'utilisateur confirme avec le nouveau password.

    POST /users/password-reset/confirm/
    Body: {"uidb64": "...", "token": "...", "password": "..."}
    """
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data['uidb64']
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']

        try:
            # 1. Décode l'ID utilisateur depuis base64
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            # 2. Vérifie que le token est valide et non expiré
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {
                        "error_code": "INVALID_TOKEN",
                        "message": "Le lien de réinitialisation est invalide ou a expiré."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 3. Le password a déjà été validé dans le serializer.validate_password()
            # Donc on peut directement le changer

            # 4. Change le mot de passe
            user.set_password(password)
            user.save()

            return Response(
                {"message": "Le mot de passe a été réinitialisé avec succès."},
                status=status.HTTP_200_OK
            )

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            # Erreur lors du décodage ou utilisateur inexistant
            return Response(
                {
                    "error_code": "INVALID_TOKEN",
                    "message": "Le lien de réinitialisation est invalide."
                },
                status=status.HTTP_400_BAD_REQUEST
            )