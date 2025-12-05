# TUTORIEL - Comment Lancer le Projet Blackjack

## Prérequis

Avant de commencer, vérifiez que vous avez:
- ✅ **Python 3.9+** installé ([télécharger ici](https://www.python.org/downloads/))
- ✅ **Git** installé ([télécharger ici](https://git-scm.com/))
- ✅ Un terminal (PowerShell, CMD, ou Bash)

**Vérifier votre version Python:**
```bash
python --version
```
Pour toutes les commandes python si vous avez une erreur essayer py à la place de python

---

## Étape 1: Cloner le Projet

Ouvrez un terminal et exécutez:

```bash
git clone https://github.com/giuuulian/BlackJack.git
cd BlackJack/blackjack_project
```

Vous devriez avoir une structure comme ça:
```
BlackJack/
├── blackjack_project/
│   ├── manage.py
│   ├── requirements.txt
│   ├── setup.py
│   ├── create_db.py
│   ├── db.sqlite3
│   └── blackjack_app/
└── [autres fichiers]
```

---

## Étape 2: Créer l'Environnement Virtuel

L'environnement virtuel isole les dépendances du projet.

**Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```bash
python -m venv venv
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

✅ **Résultat:** Votre terminal affiche `(venv)` au début

```
(venv) C:\...\BlackJack\blackjack_project>
```

---

## Étape 3: Installer les Dépendances

Toujours dans le dossier `blackjack_project` avec `(venv)` actif:

```bash
pip install -r requirements.txt
```

Cela installe:
- Django (framework web)
- bcrypt (sécurité mots de passe)
- python-dotenv (variables d'environnement)
- Et d'autres dépendances...

⏳ Cela peut prendre **2-3 minutes** la première fois.

---

## Étape 4: Initialiser la Base de Données

Créer les tables et les comptes de test:

```bash
python setup.py 
```
ou
```bash
py setup.py 
```

✅ **Résultat attendu:**
```
Création des tables de la base de données...
✓ Tables créées avec succès

Création d'un utilisateur admin...
✓ Utilisateur admin créé:
  Email: admin@example.com
  Mot de passe: Admin123!@#

Création d'un utilisateur test...
✓ Utilisateur test créé:
  Email: user@example.com
  Mot de passe: User123!@#
```

Si ça affiche "déjà présent", c'est normal (la DB existe déjà).

---

## Étape 5: Lancer le Serveur

Toujours avec `(venv)` actif:

```bash
python manage.py runserver
```

✅ **Résultat attendu:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## Étape 6: Accéder à l'Application

Ouvrez votre navigateur et allez à:

```
http://127.0.0.1:8000/
```

🎉 Vous devez voir la page d'accueil du Blackjack!

---

## Étape 7: Se Connecter

### Utilisateur Administrateur

```
📧 Email:    admin@example.com
🔐 Mot de passe: Admin123!@#
```

**Accès:** 
- Page du jeu: ✅
- Admin Panel: ✅ (visible dans la navbar)

### Utilisateur Normal

```
📧 Email:    user@example.com
🔐 Mot de passe: User123!@#
```

**Accès:**
- Page du jeu: ✅
- Admin Panel: ❌ (accès refusé 403)

---

## Étape 8: Jouer!

1. Connectez-vous avec l'un des comptes ci-dessus
2. Allez à `/game/` (ou cliquez "Jouer" dans la navbar)
3. Entrez une mise (ex: 10€)
4. Cliquez "Commencer une partie"
5. Jouez en cliquant "Tirer" ou "Rester"

**Votre solde:** Commence à 1000€
- **Si vous gagnez:** +mise
- **Si vous perdez:** -mise

---

## 🛑 Arrêter le Serveur

Dans le terminal où tourne le serveur, appuyez sur:
```
CTRL + C
```

Pour relancer le serveur (après fermeture):
```bash
# (assurez-vous d'être dans le dossier blackjack_project avec venv activé)
python manage.py runserver
```

---

## Démarrages Suivants (Raccourci)

Après la première installation, pour relancer le projet:

**Windows:**
```bash
cd C:\...\BlackJack\blackjack_project
venv\Scripts\Activate.ps1
python manage.py runserver
```

**Mac/Linux:**
```bash
cd ~/BlackJack/blackjack_project
source venv/bin/activate
python manage.py runserver
```

---

## URLs Principales

Une fois connecté, vous pouvez accéder à:

| Page | URL | Accès |
|------|-----|-------|
| 🏠 Accueil | `http://localhost:8000/` | Tous |
| 📝 Inscription | `http://localhost:8000/register/` | Pas connecté |
| 🔓 Connexion | `http://localhost:8000/login/` | Pas connecté |
| 🎮 Jeu | `http://localhost:8000/game/` | Connecté |
| 👨‍💼 Admin Panel | `http://localhost:8000/admin/dashboard/` | Admin seulement |
| ⚖️ Mentions Légales | `http://localhost:8000/legal/` | Tous |

---

## ❌ Problèmes Courants & Solutions

### ❌ "python: command not found"
```
Cause: Python n'est pas installé ou pas en PATH
Solution: Télécharger Python depuis python.org et réinstaller
         Cocher "Add Python to PATH" pendant l'installation
```

### ❌ "ModuleNotFoundError: No module named 'django'"
```
Cause: Les dépendances ne sont pas installées ou venv pas activé
Solution: Vérifier que (venv) s'affiche au début du terminal
         Relancer: pip install -r requirements.txt
```

### ❌ "Address already in use"
```
Cause: Le port 8000 est déjà utilisé (serveur déjà lancé?)
Solution: Fermer l'autre instance avec CTRL+C
         Ou utiliser un autre port: python manage.py runserver 8001
```

### ❌ "No such table: blackjack_app_user"
```
Cause: La base de données n'est pas initialisée
Solution: Relancer: python setup.py
```

### ❌ "Page indisponible" sur localhost:8000
```
Cause: Le serveur Django n'est pas lancé
Solution: Vérifier que "Starting development server" s'affiche
         Relancer: python manage.py runserver
```

---

## 🔒 Sécurité Implémentée

Ce projet inclut plusieurs protections:

✅ **Mots de passe:** Hachés avec bcrypt (jamais en clair)
✅ **Sessions:** Sécurisées (HttpOnly, Secure, SameSite)
✅ **Requêtes SQL:** Protégées contre les injections
✅ **Formulaires:** Tokens CSRF (anti-attaque)
✅ **Contenu:** Protégé contre XSS
✅ **Headers HTTP:** Sécurité renforcée

Pour plus de détails, voir `GUIDE_UTILISATION.md` → section "Sécurité Implémentée".

---

## ✅ Checklist de Vérification

Après le lancement, vérifiez que:

- [ ] Le serveur démarre sans erreur
- [ ] Vous pouvez accéder à `http://localhost:8000`
- [ ] Vous pouvez vous connecter avec `admin@example.com` / `Admin123!@#`
- [ ] Vous pouvez jouer au Blackjack
- [ ] Vous pouvez accéder à `/admin/dashboard/` en tant qu'admin
- [ ] Les utilisateurs normaux ne peuvent pas accéder à `/admin/dashboard/`

---

