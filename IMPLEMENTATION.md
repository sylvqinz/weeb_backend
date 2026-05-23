# Implémentations techniques

Ce document résume les choix techniques déjà mis en place dans le backend.

## Authentification et autorisations

Le projet utilise Django REST Framework avec une authentification JWT.

Dans `weeb_backend/settings.py`, toutes les routes API sont protégées par défaut :

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

Cela signifie que, par défaut, une route API demande un utilisateur connecté avec un token JWT valide.

## Routes publiques existantes

Certaines routes doivent rester accessibles sans être connecté.

Dans `users/views.py`, on importe :

```python
from rest_framework.permissions import AllowAny
```

Puis on ajoute :

```python
permission_classes = [AllowAny]
```

sur les vues publiques suivantes :

```text
POST /users/login/
POST /users/register/
POST /users/password-reset/request/
POST /users/password-reset/confirm/
```

Ces routes sont publiques parce qu'un utilisateur non connecté doit pouvoir :

- se connecter
- créer un compte
- demander une réinitialisation de mot de passe
- confirmer une réinitialisation de mot de passe

## Logique à respecter pour les futures routes

La règle générale est :

```text
Privé par défaut.
Public uniquement si la route déclare explicitement AllowAny.
```

Quand le blog/articles sera implémenté, les routes de lecture devront être publiques :

```text
GET /articles/
GET /articles/:id/
```

Les routes d'écriture devront rester protégées :

```text
POST /articles/
PUT /articles/:id/
PATCH /articles/:id/
DELETE /articles/:id/
```

Quand le formulaire de contact sera implémenté, son endpoint devra être public :

```text
POST /contact/
```

Il devra donc utiliser :

```python
permission_classes = [AllowAny]
```

## Rôle du frontend

Le frontend gère l'accès aux pages visibles par l'utilisateur.

Si un utilisateur n'est pas connecté, il doit uniquement pouvoir accéder aux pages :

```text
/
/contact
/login
/signup
/blog
/blog/:id
```

Toutes les autres pages doivent rediriger vers :

```text
/login
```

Le frontend contrôle la navigation, mais la vraie sécurité doit toujours être assurée côté backend.
