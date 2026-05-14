from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class UppercaseValidator:
    """
    Validateur personnalisé pour Django qui vérifie la présence d'au moins une lettre majuscule.
    
    Ce validateur est destiné à être utilisé dans la configuration Django AUTH_PASSWORD_VALIDATORS
    pour renforcer les règles de complexité des mots de passe. Il s'appuie sur les conventions
    de l'interface des validateurs de Django en implémentant les méthodes validate() et 
    get_help_text().
    
    Methods:
        validate: Vérifie que le mot de passe contient au moins une majuscule.
        get_help_text: Retourne le message d'aide à afficher à l'utilisateur.
    
    Example:
        # Dans Django settings.py:
        AUTH_PASSWORD_VALIDATORS = [
            # ...
            {
                'NAME': 'users.validators.UppercaseValidator',
            },
        ]
    """
    def validate(self, password, user=None):
        """
        Valide que le mot de passe contient au moins une lettre majuscule.
        
        Cette méthode est appelée par Django lors de la validation de tout mot de passe.
        Elle vérifie que le mot de passe fourni n'est pas une version purement minuscule
        de lui-même, ce qui signifierait l'absence de majuscules.
        
        Args:
            password (str): Le mot de passe en clair à valider.
            user (User, optional): L'instance utilisateur associée au mot de passe.
                                  Peut être None lors de la création. Défaut: None.
        
        Returns:
            None: Ne retourne rien si la validation réussit.
        
        Raises:
            ValidationError: Si le mot de passe ne contient pas de majuscule, avec:
                           - message: Message d'erreur en texte français
                           - code: 'password_no_upper' pour identification programmatique
        
        Example:
            >>> validator = UppercaseValidator()
            >>> validator.validate('password123')
            # Lève ValidationError - pas de majuscule
            
            >>> validator.validate('Password123')
            # Valide silencieusement - contient majuscule 'P'
        """
        # Si le mot de passe est identique à sa version en minuscules,
        # c'est qu'il ne contient aucune majuscule.
        if password == password.lower():
            raise ValidationError(
                _("Le mot de passe doit contenir au moins une lettre majuscule."),
                code='password_no_upper',
            )

    def get_help_text(self):
        """
        Retourne le message d'aide à afficher à l'utilisateur concernant cette règle.
        
        Ce message est destiné à être affiché dans l'interface utilisateur ou la 
        documentation API pour expliquer les exigences de complexité du mot de passe.
        
        Returns:
            str: Message d'aide expliquant l'exigence de majuscule.
        
        Example:
            >>> validator = UppercaseValidator()
            >>> help_text = validator.get_help_text()
            >>> print(help_text)
            'Votre mot de passe doit contenir au moins une lettre majuscule.'
        """
        return _(
            "Votre mot de passe doit contenir au moins une lettre majuscule."
        )

class SpecialCharacterValidator:
    """
    Validateur personnalisé pour Django qui vérifie la présence d'au moins un caractère spécial.
    
    Ce validateur est destiné à être utilisé dans la configuration Django AUTH_PASSWORD_VALIDATORS
    pour renforcer les règles de complexité des mots de passe. Il s'appuie sur les conventions
    de l'interface des validateurs de Django en implémentant les méthodes validate() et 
    get_help_text().
    
    Un caractère spécial est défini comme tout caractère qui n'est pas alphanumérique
    (i.e., pas une lettre majuscule, minuscule ou un chiffre).
    
    Methods:
        validate: Vérifie que le mot de passe contient au moins un caractère spécial.
        get_help_text: Retourne le message d'aide à afficher à l'utilisateur.
    
    Example:
        # Dans Django settings.py:
        AUTH_PASSWORD_VALIDATORS = [
            # ...
            {
                'NAME': 'users.validators.SpecialCharacterValidator',
            },
        ]
    """
    def validate(self, password, user=None):
        """
        Valide que le mot de passe contient au moins un caractère spécial.
        
        Cette méthode est appelée par Django lors de la validation de tout mot de passe.
        Elle vérifie que le mot de passe contient au moins un caractère qui n'est pas
        alphanumérique (lettres ou chiffres), comme !@#$%^&*, etc.
        
        Args:
            password (str): Le mot de passe en clair à valider.
            user (User, optional): L'instance utilisateur associée au mot de passe.
                                  Peut être None lors de la création. Défaut: None.
        
        Returns:
            None: Ne retourne rien si la validation réussit.
        
        Raises:
            ValidationError: Si le mot de passe ne contient pas de caractère spécial, avec:
                           - message: Message d'erreur en texte français
                           - code: 'password_no_special' pour identification programmatique
        
        Example:
            >>> validator = SpecialCharacterValidator()
            >>> validator.validate('Password123')
            # Lève ValidationError - pas de caractère spécial
            
            >>> validator.validate('Password123!')
            # Valide silencieusement - contient caractère spécial '!'
        """
        # Vérifie la présence d'au moins un caractère qui n'est pas alphanumérique
        if password.isalnum():
            raise ValidationError(
                _("Le mot de passe doit contenir au moins un caractère spécial."),
                code='password_no_special',
            )

    def get_help_text(self):
        """
        Retourne le message d'aide à afficher à l'utilisateur concernant cette règle.
        
        Ce message est destiné à être affiché dans l'interface utilisateur ou la 
        documentation API pour expliquer les exigences de complexité du mot de passe.
        
        Returns:
            str: Message d'aide expliquant l'exigence de caractère spécial.
        
        Example:
            >>> validator = SpecialCharacterValidator()
            >>> help_text = validator.get_help_text()
            >>> print(help_text)
            'Votre mot de passe doit contenir au moins un caractère spécial.'
        """
        return _(
            "Votre mot de passe doit contenir au moins un caractère spécial."
        )