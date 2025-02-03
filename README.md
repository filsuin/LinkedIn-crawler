# LinkedIn Job Crawler 🔍

Un outil de recherche d'emploi automatisé pour LinkedIn permettant de récupérer des offres d'emploi selon des mots-clés.

## 🚀 Fonctionnalités

- Recherche multi-mots clés
- Gestion des variations (majuscules/minuscules, tirets)
- Support français/anglais
- Variations courantes des termes techniques
- Sauvegarde automatique des résultats

## 📋 Prérequis

- Python 3.7+
- Google Chrome
- Compte LinkedIn actif
- Windows, macOS ou Linux

## 💻 Installation

1. Clonez le repository
```bash
git clone https://github.com/votre-username/LinkedIn-crawler.git
cd LinkedIn-crawler
```
2. Installez les dépendances requises
```bash
pip install selenium webdriver-manager
```
⚙️ Configuration

1. Assurez-vous d'avoir Google Chrome installé sur votre système

2. Préparez vos identifiants LinkedIn :
- Votre email
- Votre mot de passe

3. Réfléchissez à vos mots-clés de recherche

🔧 Utilisation

1. Lancez le script :
```bash
python linkedin.py
```
2. Suivez les instructions dans le terminal :
- Entrez votre email LinkedIn
- Entrez votre mot de passe
- Entrez vos mots-clés de recherche (séparés par des espaces)

📝 Exemple de mots-clés

`python développeur`
`cyber security`
`fullstack javascript`
`devops ingénieur`

⚠️ Limitations

- Respectez les conditions d'utilisation de LinkedIn
- Évitez les requêtes trop fréquentes
- Les résultats peuvent varier selon votre localisation

🐛 Résolution des problèmes courants

- Erreur de ChromeDriver : Assurez-vous d'avoir la dernière version de Chrome
- Problème de connexion : Vérifiez vos identifiants LinkedIn
- Aucun résultat : Essayez des mots-clés différents ou plus généraux
