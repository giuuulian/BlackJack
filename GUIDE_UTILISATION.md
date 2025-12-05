# 📋 GUIDE D'UTILISATION - Blackjack Sécurisé

## 🎮 Accès Rapide

**URL:** http://localhost:8000

### Comptes de Test (Créés Automatiquement)

```
┌─────────────────────┬───────────────────┬──────────────────┐
│ Rôle                │ Email             │ Mot de passe     │
├─────────────────────┼───────────────────┼──────────────────┤
│ ADMIN               │ admin@example.com │ Admin123!@#      │
│ USER                │ user@example.com  │ User123!@#       │
└─────────────────────┴───────────────────┴──────────────────┘
```

---

## 🚀 Démarrage du Projet

### Première fois (Installation Complète)

```bash
cd c:\wamp64\www\blackjack\blackjack_project

# 1. Créer l'environnement virtuel
python -m venv venv
venv\Scripts\activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer la base de données
python create_db.py

# 4. Initialiser les tables et comptes
python setup.py

# 5. Démarrer le serveur
python manage.py runserver
```

### Démarrages Suivants (Rapide)

```bash
cd c:\wamp64\www\blackjack\blackjack_project
venv\Scripts\activate
python manage.py runserver
```

### URL d'Accès

```
Accueil:         http://localhost:8000
Inscription:     http://localhost:8000/register/
Connexion:       http://localhost:8000/login/
Jeu:             http://localhost:8000/game/
Admin Panel:     http://localhost:8000/admin/dashboard/
Mentions Légales: http://localhost:8000/legal/
```

---

## 📱 Navigation sur le Site

### 1️⃣ Page d'Accueil
- Redirige automatiquement vers `/login` si pas connecté
- Affiche navbar avec boutons Connexion/Inscription

### 2️⃣ Page d'Inscription (`/register/`)

**À faire:**
1. Entrer votre **email** (format valid@email.com)
2. Entrer votre **nom** (min 2 caractères)
3. Entrer votre **mot de passe** robuste:
   - Minimum **12 caractères**
   - Au moins **3 types** de caractères (majuscules, minuscules, chiffres, spéciaux)
   - Exemple valide: `SecurePass123!`
4. **COCHER** la case "J'accepte les conditions..." (NON pré-cochée)
5. Cliquer **"Créer mon compte"**

**Messages d'erreur possibles:**
- "Email invalide" → Entrez un format valide (test@example.com)
- "Email déjà utilisé" → Cet email a un compte, allez à la connexion
- "Mot de passe trop court" → Minimum 12 caractères
- "Mot de passe faible" → Besoin de 3 types de caractères (maj/min/chiffres/spéciaux)
- "Consentement requis" → Cochez la case de consentement

**Sécurité:**
- ✅ Le mot de passe est haché avec **bcrypt** avant d'être stocké
- ✅ Jamais affichée en clair
- ✅ Consentement RGPD explicite (checkbox déjà décochée)

### 3️⃣ Page de Connexion (`/login/`)

**À faire:**
1. Entrer votre **email**
2. Entrer votre **mot de passe**
3. Cliquer **"Se connecter"**

**Messages d'erreur:**
- "Email ou mot de passe incorrect" → Email ou mot de passe mauvais (message générique pour sécurité)

**Sécurité:**
- ✅ Vérification côté serveur (pas juste JavaScript)
- ✅ Message d'erreur générique (ne révèle pas si email/password est faux)
- ✅ Session sécurisée créée (HttpOnly, Secure, SameSite)

### 4️⃣ Page du Jeu (`/game/`) - 🎰 ACCÈS SEULEMENT SI CONNECTÉ

#### 📊 Affichage

```
┌─────────────────────────────────────────────┐
│ ♠️ Blackjack                                │
│ ─────────────────────────────────────────── │
│ ┌──────────────┐          ┌──────────────┐ │
│ │  CROUPIER    │          │   VOUS       │ │
│ │  ♠️ 7  ♠️ ?  │          │  ♥️ K ♦️ Q  │ │
│ │  Score: 7   │          │  Score: 20  │ │
│ └──────────────┘          └──────────────┘ │
│                                             │
│ Solde: 1000 €                              │
│ Mise: [10]  [Commencer une partie]        │
│                                             │
│ [Tirer une carte] [Rester] [Nouvelle]     │
└─────────────────────────────────────────────┘
```

#### 🎮 Comment Jouer

1. **Entrer une mise** (1-1000 €) dans le champ "Mise"
2. **Cliquer "Commencer une partie"**
   - Vous recevez 2 cartes
   - Croupier affiche 1 carte (la 2ème est cachée)
3. **Choisir une action:**
   - **Tirer** = Ajouter une carte à votre main
   - **Rester** = Arrêter et laisser le croupier jouer
4. **Résultat:**
   - ✅ Vous avez gagné (votre score > croupier ou croupier > 21)
   - ❌ Vous avez perdu (votre score > 21 ou croupier > votre score)
   - = Égalité (même score)
5. **Nouveau jeu** = Partie suivante (solde mis à jour)

#### 📈 Solde

- **Début:** 1000 €
- **Si vous gagnez:** Solde + mise
- **Si vous perdez:** Solde - mise
- **Dépassez 21:** Vous perdez immédiatement

#### 🎯 Règles

- **Objectif:** Obtenir 21 ou le plus proche sans dépasser
- **Cartes 2-10:** Valeur face
- **Figure (J, Q, K):** 10 points
- **As (A):** 1 ou 11 points (adapté automatiquement)

**Exemple:**
```
Main: [As] [Roi] = 11 + 10 = 21 ✓ BLACKJACK!
Main: [9] [8] [6] = 9 + 8 + 6 = 23 ✗ BUST (dépassé)
```

### 5️⃣ Tableau de Bord Admin (`/admin/dashboard/`) - 👨‍💼 ADMIN SEULEMENT

**Accès:** Cliquer "Admin" dans la navbar (visible si vous êtes ADMIN)

**Affichage:**
- Liste de **TOUS les utilisateurs** du site
- Colonnes: Email, Nom, Rôle, Date inscription
- Totalement lisible et organisé

**Sécurité:**
- ✅ Vérification serveur du rôle ADMIN
- ✅ Les USER ne peuvent pas accéder (erreur 403)

**Tester l'accès refusé:**
1. Connectez-vous avec `user@example.com`
2. Allez à `/admin/dashboard/`
3. Résultat: "403 - Accès Refusé"

### 6️⃣ Page Mentions Légales (`/legal/`)

**Contenu:**
- Identité de l'éditeur
- Données collectées (Email, Nom, Mot de passe)
- Utilisation des données
- Sécurité (bcrypt)
- Conservation (durée du compte)
- Vos droits RGPD
- Cookies (HttpOnly, Secure, SameSite)
- Contact

**Accès:** Lien dans le footer (visible partout)

---

## 🔐 Sécurité Implémentée

### ✅ Authentification (Sessions Sécurisées)

```javascript
// Cookie Session (F12 > Application > Cookies > localhost)
Attributs:
- HttpOnly:  ✓ (inaccessible JavaScript)
- Secure:    ✓ (HTTPS seulement)
- SameSite:  ✓ (Strict = anti-CSRF)
- Expires:   30 min d'inactivité
```

**Comment vérifier:**
1. F12 (Ouvrir DevTools)
2. Onglet "Application" → Cookies
3. Vérifier la session cookie

### ✅ Mots de Passe (Bcrypt)

```bash
# Vérifier en base (SQLite):
db.sqlite3 (fichier contient les hashes bcrypt)

# Exemple de hash bcrypt:
$2b$12$AbCdEfGhIjKlMnOpQrStUv...
# Jamais en clair, jamais MD5/SHA1
```

### ✅ Requêtes SQL (Injection SQL Protégée)

```python
# Utilisé dans l'app:
User.objects.filter(email=email)  # ORM Django
# ✅ Paramètres séparés de la requête
# ✅ Automatiquement échappée
```

### ✅ XSS (Cross-Site Scripting Protégé)

**Test XSS:**
1. Vous inscrire avec un nom contenant `<script>alert('XSS')</script>`
2. Vous connecter
3. Voir le profil
4. Résultat: Texte brut affiché (pas d'alerte)

### ✅ CSRF (Tokens CSRF)

```html
<!-- Dans chaque formulaire POST: -->
<input type="hidden" name="csrftoken" value="...">
<!-- Validé automatiquement côté serveur -->
```

### ✅ Headers de Sécurité HTTP

```
Vérifier en F12 > Network > Request > Response Headers:
X-Content-Type-Options: nosniff       ✓
X-Frame-Options: DENY                 ✓
X-XSS-Protection: 1; mode=block       ✓
```

---

## 🛠️ Fichiers Importants

```
blackjack_project/
├── .env                    ← Configuration (GIT IGNORED)
├── .env.example            ← Exemple .env (dans Git)
├── .gitignore              ← Exclut .env, certs, logs
├── requirements.txt        ← Dépendances (Django, bcrypt, etc.)
│
├── blackjack_app/
│   ├── models.py          ← User, GameSession (tables)
│   ├── views.py           ← Login, Register, Game, Admin
│   ├── api_views.py       ← API jeu (start, hit, stand)
│   ├── forms.py           ← Formulaires + validation
│   ├── middleware.py      ← Headers sécurité HTTP
│   └── validators.py      ← Validation mot de passe
│
├── templates/
│   ├── base.html          ← Template de base (nav, footer)
│   ├── register.html      ← Formulaire inscription
│   ├── login.html         ← Formulaire connexion
│   ├── game.html          ← Jeu Blackjack
│   ├── admin_dashboard.html ← Panel admin
│   ├── legal.html         ← Mentions légales
│   └── *.html             ← Pages erreur (403, 404, 500)
│
└── db.sqlite3             ← Base de données SQLite
```

---

## ❌ Problèmes Courants & Solutions

### ❌ "Page Not Found"
```
Cause: Vous êtes sur la mauvaise URL
Solution: Allez à http://localhost:8000
```

### ❌ "Email ou mot de passe incorrect"
```
Cause: Email et/ou mot de passe faux
Solution: Vérifier les comptes de test (voir haut)
```

### ❌ "Le mot de passe doit contenir au moins 12 caractères"
```
Cause: Mot de passe trop court
Solution: Utiliser minimum 12 caractères + 3 types
Exemple: SecurePass123! ✓
```

### ❌ "Consentement requis"
```
Cause: Vous n'avez pas coché la case consentement
Solution: Cocher la checkbox avant soumettre
```

### ❌ "403 - Accès Refusé"
```
Cause: Vous essayez d'accéder à /admin/ sans être ADMIN
Solution: Connectez-vous avec admin@example.com
```

### ❌ "Erreur serveur"
```
Cause: Erreur interne (logs dans logs/error.log)
Solution: Vérifier que Django tourne (python manage.py runserver)
```

---

## 📊 Checklist de Validation Sécurité

Avant de soumettre le projet:

### Authentification
- [ ] Login fonctionne avec email + mot de passe
- [ ] Register valide email et mot de passe fort
- [ ] Consentement checkbox existe et est NON pré-coché
- [ ] Mots de passe en bcrypt (vérifier en base)
- [ ] Sessions timeout après 30 min

### Données
- [ ] Formulaires valident les entrées côté serveur
- [ ] Messages d'erreur ne révèlent pas d'infos sensibles
- [ ] XSS impossible (test avec <script>)

### Contrôle d'Accès
- [ ] 2 rôles existentes (USER et ADMIN)
- [ ] Admin panel visible seulement si ADMIN
- [ ] USER ne peut pas accéder /admin/ (403)

### Configuration
- [ ] .env en .gitignore (pas en clair dans Git)
- [ ] .env.example documenté (dans Git)
- [ ] Pas d'erreurs Python affichées à l'utilisateur

### Sécurité HTTP
- [ ] Headers X-Content-Type-Options, X-Frame-Options présents

---

## 🎯 Résumé Technique

| Aspect | Implémentation | Status |
|--------|----------------|--------|
| Backend | Django 4.2.7 | ✅ |
| Frontend | HTML + Bootstrap 5 + JavaScript vanilla | ✅ |
| Base de données | SQLite (développement) | ✅ |
| Authentification | Sessions Django + bcrypt | ✅ |
| Mots de passe | Bcrypt (12 rounds) | ✅ |
| Requêtes SQL | ORM Django (préparées) | ✅ |
| XSS | Autoescape Django | ✅ |
| CSRF | Tokens Django auto | ✅ |
| Sessions | HttpOnly, Secure, SameSite | ✅ |
| Erreurs | Messages génériques | ✅ |
| Logs | Fichier logs/error.log | ✅ |

---

## 📞 Support

Si une erreur:
1. Vérifier que Django tourne: `python manage.py runserver`
2. Vérifier les logs: `cat logs/error.log`
3. Vérifier la connexion database: `db.sqlite3` existe
4. Redémarrer le serveur et rafraîchir la page

---

**Bonne chance! 🍀**

Enjoy the blackjack game! 🎰
