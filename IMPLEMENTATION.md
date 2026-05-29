# Implémentations techniques

Ce document sert de sommaire pour les choix techniques déjà mis en place dans le backend.

## Documentation

- [Modèle utilisateur personnalisé](docs/USER_MODEL.md)
- [Authentification et autorisations](docs/AUTH.md)
- [Politique de mots de passe](docs/PASSWORD_POLICY.md)
- [Reset password par email](docs/PASSWORD_RESET.md)
- [Gestion des secrets avec `.env`](docs/ENVIRONMENT.md)
- [Connexion avec le frontend local](docs/FRONTEND_BACKEND.md)

## Résumé rapide

Le backend utilise :

- Django REST Framework avec JWT
- un modèle `CustomUser` basé sur l'email
- une politique de mots de passe renforcée
- un reset password par email avec token Django
- `python-decouple` pour externaliser les secrets
- `django-cors-headers` pour connecter le frontend local
