from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class UppercaseValidator:
    """
    Validateur qui vérifie la présence d'au moins une lettre majuscule.
    """
    def validate(self, password, user=None):
        # Si le mot de passe est identique à sa version en minuscules,
        # c'est qu'il ne contient aucune majuscule.
        if password == password.lower():
            raise ValidationError(
                _("Le mot de passe doit contenir au moins une lettre majuscule."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Votre mot de passe doit contenir au moins une lettre majuscule."
        )

class SpecialCharacterValidator:
    """
    Validateur qui vérifie la présence d'au moins un caractère spécial.
    """
    def validate(self, password, user=None):
        # Vérifie la présence d'au moins un caractère qui n'est pas alphanumérique
        if password.isalnum():
            raise ValidationError(
                _("Le mot de passe doit contenir au moins un caractère spécial."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            "Votre mot de passe doit contenir au moins un caractère spécial."
        )