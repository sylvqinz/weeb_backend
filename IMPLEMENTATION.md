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

## Reset password par email

La demande de réinitialisation se fait en deux étapes :

```text
POST /users/password-reset/request/
POST /users/password-reset/confirm/
```

`POST /users/password-reset/request/` reçoit un email, génère un `uidb64` et un token Django, puis envoie un lien au frontend :

```text
{FRONTEND_URL}/reset-password?uidb64={uidb64}&token={token}
```

La réponse reste toujours générique, même si l'email n'existe pas, pour éviter l'énumération d'utilisateurs.

L'envoi est fait dans `users/views.py` avec `django.core.mail.send_mail`.

Le contenu envoyé contient :

- un sujet de réinitialisation
- un court message explicatif
- le lien de reset contenant `uidb64` et `token`
- une phrase indiquant d'ignorer l'email si la demande ne vient pas de l'utilisateur

En cas d'échec SMTP, l'erreur est loggée côté serveur, mais la réponse API reste générique pour ne pas révéler si l'email existe.

La configuration d'envoi est dans `weeb_backend/settings.py` via les variables :

```text
EMAIL_BACKEND
EMAIL_HOST
EMAIL_PORT
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
EMAIL_USE_TLS
EMAIL_USE_SSL
DEFAULT_FROM_EMAIL
FRONTEND_URL
```

Par défaut en local, `EMAIL_BACKEND` utilise `django.core.mail.backends.console.EmailBackend`.

Pour envoyer de vrais emails via Gmail SMTP, les variables attendues dans `.env` sont :

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=adresse-gmail-du-projet@gmail.com
EMAIL_HOST_PASSWORD=mot-de-passe-application-google
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=Weeb <adresse-gmail-du-projet@gmail.com>
```

`EMAIL_HOST_PASSWORD` doit être un mot de passe d'application Google, pas le mot de passe normal du compte Gmail.

Ces valeurs ne doivent jamais être commit dans Git. Elles restent uniquement dans le fichier `.env` local ou dans les variables d'environnement de production.

### Test SMTP

Pour tester l'envoi SMTP depuis Django :

```bash
python3 manage.py shell
```

Puis :

```python
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    "Test SMTP Weeb",
    "Si tu reçois ce mail, Gmail SMTP fonctionne.",
    settings.DEFAULT_FROM_EMAIL,
    ["adresse-de-test@example.com"],
    fail_silently=False,
)
```

Si la commande retourne `1`, l'email a été accepté par le serveur SMTP.

Sur macOS, si Python retourne une erreur de certificat SSL, il faut utiliser les certificats du virtualenv :

```bash
source .venv/bin/activate
python3 -m pip install --upgrade certifi
export SSL_CERT_FILE=$(python3 -m certifi)
```

### URL frontend

`FRONTEND_URL` doit pointer vers l'application frontend qui affiche le formulaire de nouveau mot de passe.

En local, avec un frontend lancé séparément :

```env
FRONTEND_URL=http://localhost:3000
```

ou, pour Vite :

```env
FRONTEND_URL=http://localhost:5173
```

Le frontend doit avoir une route `/reset-password` qui lit les paramètres `uidb64` et `token`, puis appelle :

```text
POST /users/password-reset/confirm/
```

avec :

```json
{
  "uidb64": "...",
  "token": "...",
  "password": "NouveauMotDePasse123!"
}
```

En production, `FRONTEND_URL` devra être remplacé par l'URL publique du frontend.

## Connexion avec le frontend local

Le backend autorise les appels depuis un frontend local via `django-cors-headers`.

La dépendance est ajoutée dans `requirements.txt` :

```text
django-cors-headers
```

Dans `weeb_backend/settings.py`, l'application et le middleware sont activés :

```python
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    ...
]
```

Les origines locales autorisées par défaut sont :

```text
http://localhost:3000
http://127.0.0.1:3000
http://localhost:5173
http://127.0.0.1:5173
```

Elles peuvent être remplacées dans `.env` avec :

```env
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

`CORS_ALLOW_CREDENTIALS = True` est activé pour permettre au navigateur d'accepter les cookies définis par le backend, notamment le cookie `refresh_token`.

Dans le repo frontend, une variable d'environnement doit pointer vers l'API backend locale :

```env
VITE_API_URL=http://127.0.0.1:8000
```

Les routes backend utilisées par le frontend sont :

```text
POST /users/register/
POST /users/login/
POST /users/password-reset/request/
POST /users/password-reset/confirm/
```

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
