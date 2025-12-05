#!/usr/bin/env python
"""
Run Django development server with SSL/HTTPS support
"""
import os
import sys
import ssl
from pathlib import Path

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blackjack_project.settings')

import django
django.setup()

from django.core.management.commands.runserver import Command as RunServerCommand
from django.core.wsgi import get_wsgi_application
from werkzeug.serving import run_simple

def main():
    """Run the development server with HTTPS"""
    
    cert_file = Path('certs/localhost.crt')
    key_file = Path('certs/localhost.key')
    
    print("\n" + "="*70)
    print("🎰 BLACKJACK SÉCURISÉ - Serveur HTTPS")
    print("="*70)
    
    if not cert_file.exists() or not key_file.exists():
        print("\n✗ Certificats non trouvés. Génération en cours...")
        os.system(f'{sys.executable} generate_certs.py')
    
    print("\n✓ Démarrage du serveur sur https://localhost:8000/\n")
    print("Comptes de test:")
    print("  • Admin: admin@example.com / Admin123!@#")
    print("  • User:  user@example.com / User123!@#")
    print("\nNOTE: Acceptez l'avertissement de sécurité du navigateur")
    print("      (certificat auto-signé en développement)")
    print("\nAppuyez sur Ctrl+C pour arrêter.\n")
    print("="*70 + "\n")
    
    try:
        # Create SSL context
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(str(cert_file), str(key_file))
        
        # Get WSGI application
        app = get_wsgi_application()
        
        # Run with Werkzeug
        run_simple(
            'localhost',
            8000,
            app,
            ssl_context=ssl_context,
            use_reloader=True,
            use_debugger=True,
            threaded=True
        )
    except Exception as e:
        print(f"\n✗ Erreur: {e}")
        print("\nFallback: Lancement en HTTP...\n")
        from django.core.management import call_command
        call_command('runserver', '127.0.0.1:8000')

if __name__ == '__main__':
    main()
