#!/usr/bin/env python
"""
Run Django development server with HTTPS (SSL/TLS)
"""
import os
import sys
import ssl

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blackjack_project.settings')

import django
django.setup()

from django.core.management import call_command
from pathlib import Path

def run_https_server():
    """Run the development server with HTTPS"""
    
    cert_file = Path('certs/localhost.crt')
    key_file = Path('certs/localhost.key')
    
    print("\n" + "="*70)
    print("🎰 BLACKJACK SÉCURISÉ - Serveur HTTPS")
    print("="*70)
    
    if not cert_file.exists() or not key_file.exists():
        print("\n✗ Certificats non trouvés !")
        print("Génération en cours...")
        os.system(f'{sys.executable} generate_certs.py')
    
    if not cert_file.exists() or not key_file.exists():
        print("✗ Impossible de générer les certificats")
        sys.exit(1)
    
    print("\n✓ Démarrage du serveur HTTPS sur https://localhost:8000/\n")
    print("Comptes de test:")
    print("  • Admin: admin@example.com / Admin123!@#")
    print("  • User:  user@example.com / User123!@#")
    print("\nNOTE: Acceptez l'avertissement de sécurité du navigateur")
    print("      (certificat auto-signé en développement local)\n")
    print("Appuyez sur Ctrl+C pour arrêter.\n")
    print("="*70 + "\n")
    
    try:
        # Try using runserver_plus from django-extensions if available
        try:
            call_command('runserver_plus', '127.0.0.1:8000', 
                        use_ssl=True, 
                        ssl_certfile=str(cert_file),
                        ssl_keyfile=str(key_file))
        except:
            # Fallback: Use werkzeug with SSL context
            from django.core.wsgi import get_wsgi_application
            from werkzeug.serving import run_simple
            
            app = get_wsgi_application()
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(str(cert_file), str(key_file))
            
            run_simple('localhost', 8000, app, 
                      ssl_context=ssl_context,
                      use_reloader=True, 
                      use_debugger=True, 
                      threaded=True)
    except KeyboardInterrupt:
        print("\n\n✓ Serveur arrêté.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Erreur: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_https_server()
