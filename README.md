# Workflow Git

## Branches principales
- `main` → production 
- `dev` → intégration des nouvelles fonctionnalités


## Développement d’une feature

→ Se placer sur la branche `dev` et la mettre à jour :

- git checkout dev
- git pull

→ Créer une nouvelle branche :

- git checkout -b feature/nom-de-la-feature
- Développement de la fonctionnalité et commit des changements

→ Push la branche :
- git push origin feature/nom-de-la-feature

→ Ouvrir une Pull Request :
- Source : feature/nom-de-la-feature
- Target : dev
- Après review et validation → merge dans `dev`
- Suppression de la branche feature
- Close issue

## Lancement du projet

### Préparation de l'environnement Python
Sur Mac :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Sur Windows PowerShell :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Sur Windows CMD :

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Créer le .env

Créer un fichier `.env` à la racine du projet avec les variables disponible sur le drive


### Lancement

```bash
python manage.py migrate
python manage.py runserver
```

Serveur dispo sur :

```text
http://127.0.0.1:8000/
```

## Documentation technique

Les choix d'implémentation déjà réalisés sont résumés dans [IMPLEMENTATION.md](IMPLEMENTATION.md).
