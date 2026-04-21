# Workflow Git

## Branches principales
- `main` → production 
- `dev` → intégration des nouvelles fonctionnalités


## Développement d’une feature

→ Se placer sur la branche `dev` et la mettre à jour :

- git checkout dev
- git pull

→ Créer une nouvelle branche :

git checkout -b feature/nom-de-la-feature
Développement de la fonctionnalité et commit des changements

→ Push la branche :
git push origin feature/nom-de-la-feature

→ Ouvrir une Pull Request :
Source : feature/nom-de-la-feature
Target : dev
Après review et validation → merge dans `dev`

