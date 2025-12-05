#!/usr/bin/env python
"""
Setup script - Creates database tables and admin user
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blackjack_project.settings')
django.setup()

from django.core.management import call_command
from blackjack_app.models import User

def setup_database():
    """Create database tables"""
    print("Création des tables de la base de données...")
    call_command('migrate', '--run-syncdb')
    print("✓ Tables créées avec succès")

def create_admin_user():
    """Create an admin user for testing"""
    print("\nCréation d'un utilisateur admin...")
    
    admin_email = 'admin@example.com'
    admin_name = 'Administrateur'
    admin_password = 'Admin123!@#'
    
    # Check if admin already exists
    if User.objects.filter(email=admin_email).exists():
        print(f"✓ Utilisateur admin déjà présent: {admin_email}")
        return
    
    admin = User(email=admin_email, name=admin_name, role='admin')
    admin.set_password(admin_password)
    admin.save()
    
    print(f"✓ Utilisateur admin créé:")
    print(f"  Email: {admin_email}")
    print(f"  Mot de passe: {admin_password}")

def create_test_user():
    """Create a test user"""
    print("\nCréation d'un utilisateur test...")
    
    test_email = 'user@example.com'
    test_name = 'Utilisateur Test'
    test_password = 'User123!@#'
    
    # Check if user already exists
    if User.objects.filter(email=test_email).exists():
        print(f"✓ Utilisateur test déjà présent: {test_email}")
        return
    
    user = User(email=test_email, name=test_name, role='user')
    user.set_password(test_password)
    user.save()
    
    print(f"✓ Utilisateur test créé:")
    print(f"  Email: {test_email}")
    print(f"  Mot de passe: {test_password}")

if __name__ == '__main__':
    setup_database()
    create_admin_user()
    create_test_user()
    print("\n✓ Configuration terminée!")
