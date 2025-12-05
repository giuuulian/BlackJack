#!/usr/bin/env python
"""
Launch script - Start Django development server with HTTPS
"""
import os
import sys
import django
import subprocess
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blackjack_project.settings')
django.setup()

def check_certificates():
    """Check if HTTPS certificates exist"""
    cert_dir = Path('certs')
    cert_file = cert_dir / 'localhost.crt'
    key_file = cert_dir / 'localhost.key'
    
    if not cert_file.exists() or not key_file.exists():
        print("⚠️  Certificats HTTPS non trouvés.")
        print("Génération des certificats...")
        result = subprocess.run([sys.executable, 'generate_certs.py'])
        if result.returncode != 0:
            print("✗ Erreur lors de la génération des certificats.")
            sys.exit(1)

def run_server():
    """Run Django development server with HTTPS"""
    from django.core.management import call_command
    
    print("=" * 60)
    print("🎰 Blackjack Sécurisé - Serveur de développement")
    print("=" * 60)
    print("\nDémarrage du serveur HTTPS sur https://localhost:8443...")
    print("\nComptes de test:")
    print("  Admin: admin@example.com / Admin123!@#")
    print("  User:  user@example.com / User123!@#")
    print("\nAppuyez sur Ctrl+C pour arrêter le serveur.")
    print("=" * 60 + "\n")
    
    try:
        # Try to use django-extensions for HTTPS if available
        call_command('runserver_plus', 'localhost:8443', use_ssl=True)
    except:
        # Fallback to standard runserver
        print("Note: Pour HTTPS en développement, installez django-extensions:")
        print("  pip install django-extensions")
        print("\nUtilisation du serveur HTTP standard pour le moment...")
        call_command('runserver', 'localhost:8000')

if __name__ == '__main__':
    check_certificates()
    run_server()
