# 🎰 Blackjack Sécurisé - Application Django

Une application Blackjack fonctionnelle développée avec **Django** et **JavaScript vanilla**.

## ✨ Fonctionnalités Implémentées

### Système d'Authentification Robuste ✅
- **Inscription (`/register`)**
  - Validation email (format valide)
  - Mot de passe minimum 12 caractères + 3 types (majuscules, minuscules, chiffres, spéciaux)
  - Consentement RGPD explicite (checkbox NON pré-cochée)
  - Hachage bcrypt des mots de passe

- **Connexion (`/login`)**
  - Validation côté serveur
  - Messages d'erreur génériques (sécurité)
  - Vérification bcrypt du mot de passe

- **Sessions Sécurisées**
  - Attributs `HttpOnly`, `Secure`, `SameSite=Strict`
  - Timeout 30 minutes d'inactivité
  - Logout détruit complètement la session

### Système de Rôles & Contrôle d'Accès ✅
- **2 rôles:** USER et ADMIN
- **Stockage en base:** colonne `role` dans table `users`
- **Page Admin-only:** `/admin/dashboard` (affiche tous les utilisateurs)
- **Vérification serveur:** Impossible d'accéder sans être ADMIN
- **Protection IDOR:** Impossible de voir le profil d'un autre utilisateur

### Protections Contre Injections ✅
- **Requêtes SQL préparées:** Utilisation de l'ORM Django (paramètres séparés)
- **Échappement XSS:** Templates Django (autoescape par défaut)
- **Validation entrées:** Côté serveur (email, longueur, caractères)

### Conformité RGPD ✅
- **Minimisation données:** Seulement Email + Mot de passe + Nom
- **Consentement explicite:** Checkbox NON pré-cochée (obligatoire)
- **Mentions Légales:** Page `/legal` complète (droit, utilisation, conservation)
- **Fichier `.env.example`:** Documentation des variables

### Protections CSRF & Headers HTTP ✅
- **Token CSRF:** Automatique Django (dans les formulaires)
- **Headers de sécurité:**
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`

### Sécurité Fichiers & HTTPS ✅
- **HTTPS obligatoire:** Certificats auto-signés local
- **Secrets en `.env`:** JAMAIS en clair dans le code
- **`.gitignore`:** `.env` exclu du repo

### Gestion des Erreurs ✅
- **Erreurs génériques utilisateur:** Messages non-révélateurs
- **Logs serveur:** Fichier `logs/error.log`
- **Pages d'erreur custom:** 403, 404, 500

## 🎮 Le Jeu Blackjack

**Règles:**
- Joueur vs Croupier
- L'objectif: obtenir 21 ou plus proche de 21 sans dépasser
- Joker (As) = 1 ou 11 points
- Figure (J,Q,K) = 10 points

**Actions:**
1. Placer une mise (1-1000€)
2. Cliquer "Commencer" - reçoit 2 cartes
3. "Tirer" - ajouter une carte
4. "Rester" - croupier joue et gagnant déterminé
5. "Nouvelle partie" - recommencer avec balance mise à jour

**Solde:**
- Commence à 1000€
- Gagne = +mise
- Perd = -mise

## 🔒 Sécurité Implémentée

### Mots de Passe
```
✅ Hachage bcrypt (rounds=12)
✅ Jamais stockés en clair
✅ Validation force requise (12+ chars, 3 types)
✅ Vérification constanttime
```

### Requêtes SQL
```
✅ ORM Django (pas de concaténation)
✅ Paramètres séparés de la requête
✅ Protection SQL Injection automatique
```

### XSS
```
✅ Autoescape Django par défaut
✅ Variables {{ }} dans templates
✅ Validation + échappement côté serveur
```

### CSRF
```
✅ Token dans tous les formulaires
✅ Validation automatique Django
✅ Vérification `SameSite=Strict`
```

### Sessions
```
✅ HttpOnly = inaccessible JavaScript
✅ Secure = HTTPS seulement
✅ SameSite=Strict = pas de cross-site
✅ Timeout 30 min
```

## 📋 Prérequis

- **Python 3.8+**
- **MySQL (WAMP)** - base de données `blackjack`
- **pip** - gestionnaire de paquets Python
- **OpenSSL** - pour certificats HTTPS locaux

## 🚀 Installation & Démarrage

### 1. Cloner le projet
```bash
cd c:\wamp64\www\blackjack\blackjack_project
```

### 2. Créer l'environnement virtuel Python
```bash
python -m venv venv
# Activation
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Créer la base de données MySQL
```bash
# Ouvrir phpMyAdmin (http://localhost/phpmyadmin)
# OU via MySQL console:
mysql -u root -p
CREATE DATABASE blackjack;
EXIT;
```

### 5. Configurer l'environnement
```bash
# Le fichier .env est déjà configuré
# Vérifier les paramètres DB si besoin:
# DB_NAME=blackjack
# DB_USER=root
# DB_PASSWORD=  (vide si pas de mot de passe)
# DB_HOST=127.0.0.1
```

### 6. Générer les certificats HTTPS
```bash
python generate_certs.py
```

### 7. Initialiser la base de données
```bash
python setup.py
```
Cela crée les tables et deux comptes de test:
- **Admin:** admin@example.com / Admin123!@#
- **User:** user@example.com / User123!@#

### 8. Lancer le serveur
```bash
python run.py
```

Ou directement:
```bash
python manage.py runserver localhost:8000
```

### 9. Accéder au site
```
http://localhost:8000
```

## 📁 Structure du Projet

```
blackjack_project/
├── manage.py                 # CLI Django
├── requirements.txt          # Dépendances pip
├── .env                      # Configuration (GIT IGNORED)
├── .env.example              # Exemple .env
├── .gitignore                # Exclusions Git
├── generate_certs.py         # Génération certificats HTTPS
├── setup.py                  # Installation base de données
├── run.py                    # Lancer le serveur
│
├── blackjack_project/        # Configuration Django
│   ├── settings.py           # Configuration générale (SECURITY)
│   ├── urls.py               # Routes principales
│   ├── wsgi.py               # WSGI application
│   └── __init__.py
│
├── blackjack_app/            # Application principale
│   ├── models.py             # Modèles User, GameSession
│   ├── views.py              # Vues (login, register, game, admin)
│   ├── api_views.py          # API endpoints (jeu)
│   ├── urls.py               # Routes app
│   ├── forms.py              # Formulaires (validation)
│   ├── validators.py         # Validateurs personnalisés
│   ├── middleware.py         # Middleware sécurité (headers)
│   └── __init__.py
│
├── templates/                # Templates HTML
│   ├── base.html             # Template de base
│   ├── register.html         # Page inscription
│   ├── login.html            # Page connexion
│   ├── game.html             # Page jeu
│   ├── admin_dashboard.html  # Tableau de bord admin
│   ├── legal.html            # Mentions légales
│   ├── 403.html              # Erreur 403
│   ├── 404.html              # Erreur 404
│   └── 500.html              # Erreur 500
│
├── static/                   # Fichiers statiques
│   ├── css/
│   │   └── style.css         # Styles CSS
│   └── js/
│       └── game.js           # Logique jeu (JavaScript)
│
├── certs/                    # Certificats HTTPS (GIT IGNORED)
│   ├── localhost.crt
│   └── localhost.key
│
└── logs/                     # Logs serveur (GIT IGNORED)
    └── error.log
```

## 🔑 Comptes de Test

Créés automatiquement par `setup.py`:

```
📊 ADMIN
Email:    admin@example.com
Password: Admin123!@#
Accès:    /admin/dashboard

👤 USER
Email:    user@example.com
Password: User123!@#
Accès:    /game
```

## 📊 Vérification Sécurité (Checklist)

### ✅ Mots de Passe
```bash
# Vérifier le hash bcrypt en base:
mysql -u root -p blackjack
SELECT email, password_hash FROM users LIMIT 1;
# Doit afficher: $2b$12$... (hash bcrypt, pas MD5/SHA1)
```

### ✅ Requêtes SQL
```bash
# Aucune concaténation dans le code:
grep -r "SELECT.*\+" blackjack_app/
# Doit être vide (ORM Django utilisé)
```

### ✅ XSS
```
1. Aller à /game
2. Poster commentaire: <script>alert('XSS')</script>
3. Résultat: texte brut affiché (pas de popup)
```

### ✅ Headers HTTP
```bash
# En navigateur (F12 > Network > Request > Response Headers):
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
```

### ✅ .env en .gitignore
```bash
git status
# .env ne doit PAS être listé
# .env.example DOIT être présent
```

### ✅ RGPD
```
1. Inscriptionon: Email + Nom + Password SEULEMENT
2. Checkbox consentement: NON cochée par défaut
3. /legal: Mentions légales complètes
```

## 🎯 Critères Validés

| Critère | Statut | Notes |
|---------|--------|-------|
| Login/Register robuste | ✅ | bcrypt, validation serveur |
| 2 rôles + ADMIN page | ✅ | USER, ADMIN, /admin/dashboard |
| Requêtes préparées | ✅ | Django ORM |
| Échappement XSS | ✅ | Autoescape Django |
| RGPD minimisation | ✅ | Email, Nom, Password uniquement |
| Consentement non-coché | ✅ | Checkbox explicite |
| Mentions légales | ✅ | Page /legal complète |
| Headers HTTP | ✅ | X-Content-Type, X-Frame, X-XSS |
| HTTPS local | ✅ | Certificats auto-signés |
| .env en .gitignore | ✅ | Configuré correctement |
| Sessions sécurisées | ✅ | HttpOnly, Secure, SameSite |
| Protection IDOR | ✅ | Vérification user_id session |
| CSRF tokens | ✅ | Django automatique |
| Erreurs génériques | ✅ | Messages non-révélateurs |

## 🐛 Dépannage

### Erreur: "No module named 'django'"
```bash
pip install -r requirements.txt
```

### Erreur: "Access denied for user 'root'"
```bash
# Vérifier .env:
DB_PASSWORD=  # Vérifier la valeur
# Ou ajouter mot de passe WAMP si configuré
```

### Erreur: "Database 'blackjack' doesn't exist"
```bash
# Créer la base:
mysql -u root -p
CREATE DATABASE blackjack;
EXIT;
```

### HTTPS: "Certificate not found"
```bash
# Générer les certificats:
python generate_certs.py
# Require OpenSSL
```

## 📝 Documentation Sécurité Complète

Tous les points du cahier des charges sont implémentés:

1. ✅ **Architecture & Configuration** - `.env`, mode production
2. ✅ **Authentification & Sessions** - bcrypt, cookies sécurisés
3. ✅ **Contrôle d'Accès** - 2 rôles, vérification serveur
4. ✅ **Injections & Données** - ORM, validation, XSS
5. ✅ **Fonctionnalités Sensibles** - CSRF, uploads, erreurs
6. ✅ **Conformité RGPD** - Minimisation, consentement, mentions
7. ✅ **Headers HTTP** - X-Content-Type, X-Frame
8. ✅ **Déploiement** - HTTPS, secrets, production
9. ✅ **Tests Sécurité** - Code review, bonnes pratiques

## 🤝 Support

Pour tout problème, vérifier:
1. Base de données MySQL active
2. Python 3.8+ installé
3. `pip install -r requirements.txt` exécuté
4. `.env` configuré correctement
5. Certificats HTTPS générés

## 📄 Licence

Projet éducatif - 2024

---

**Développé pour respecter les critères de sécurité Web du fil rouge sécurité.**
