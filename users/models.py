from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

# --- 1. LE MANAGER ---
class CustomUserManager(BaseUserManager):
    """
    Gestionnaire personnalisé où l'email est l'identifiant unique
    pour l'authentification, à la place du nom d'utilisateur.
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("L'adresse email doit être renseignée."))
        if not password:
            raise ValueError(_("Le mot de passe doit être renseigné."))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Hache le mot de passe de façon sécurisée
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Le SuperUtilisateur doit avoir is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Le SuperUtilisateur doit avoir is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

# --- 2. LE MODÈLE USER ---
class CustomUser(AbstractUser):
    # On supprime définitivement le champ username hérité
    username = None

    # L'email reste obligatoire et unique
    email = models.EmailField(_('adresse email'), unique=True, blank=False)

    # On indique à Django que l'email est le nouvel identifiant de connexion
    USERNAME_FIELD = 'email'

    # first_name et last_name → hérités
    # is_active              → hérité
    # date_joined            → hérité (équivalent de created_at)

    # REQUIRED_FIELDS est vide car l'email et le mot de passe sont requis par défaut
    REQUIRED_FIELDS = []

    # On lie notre modèle à notre nouveau gestionnaire
    objects = CustomUserManager()

    def __str__(self):
        return self.email