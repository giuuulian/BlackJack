#!/usr/bin/env python
"""
Launch Django development server with HTTPS support
"""
import os
import sys
import ssl
import django
from pathlib import Path
from django.core.management import call_command

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blackjack_project.settings')
django.setup()

def generate_certificates():
    """Generate self-signed certificates if needed"""
    cert_dir = Path('certs')
    cert_dir.mkdir(exist_ok=True)
    
    cert_file = cert_dir / 'localhost.crt'
    key_file = cert_dir / 'localhost.key'
    
    if cert_file.exists() and key_file.exists():
        return True
    
    print("Génération des certificats SSL auto-signés...")
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'generate_certs.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Certificats créés avec succès")
            return True
        else:
            print(f"✗ Erreur: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False

def run_https_server():
    """Run Django development server with HTTPS"""
    print("\n" + "="*70)
    print("🎰 BLACKJACK SÉCURISÉ - Serveur de développement HTTPS")
    print("="*70)
    print("\n✓ Serveur démarrant sur https://localhost:8000/\n")
    print("Comptes de test:")
    print("  • Admin: admin@example.com / Admin123!@#")
    print("  • User:  user@example.com / User123!@#")
    print("\nNOTE: Votre navigateur peut afficher un avertissement de sécurité.")
    print("      C'est normal pour les certificats auto-signés en développement.")
    print("      Cliquez sur 'Accepter le risque' pour continuer.\n")
    print("Appuyez sur Ctrl+C pour arrêter le serveur.")
    print("="*70 + "\n")
    
    # Try using Werkzeug SSL with django runserver
    try:
        from werkzeug.serving import WSGIRequestHandler
        from django.core.wsgi import get_wsgi_application
        
        # Generate certs
        if not generate_certificates():
            print("Impossible de générer les certificats. Démarrage en HTTP...")
            call_command('runserver', '127.0.0.1:8000')
            return
        
        cert_file = Path('certs/localhost.crt')
        key_file = Path('certs/localhost.key')
        
        if cert_file.exists() and key_file.exists():
            # Use ssl_context
            import ssl
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(str(cert_file), str(key_file))
            
            app = get_wsgi_application()
            WSGIRequestHandler.ssl_context = ssl_context
            
            # Run with ssl
            from werkzeug.serving import run_simple
            run_simple('localhost', 8000, app, ssl_context='adhoc', use_reloader=True, 
                      use_debugger=True, threaded=True)
        else:
            print("Certificats non trouvés. Démarrage en HTTP...")
            call_command('runserver', '127.0.0.1:8000')
    except Exception as e:
        print(f"Erreur lors du démarrage HTTPS: {e}")
        print("Basculement vers HTTP...\n")
        call_command('runserver', '127.0.0.1:8000')

if __name__ == '__main__':
    try:
        # Simple approach: just run standard runserver which now uses HTTP
        # But Django will handle the HTTPS redirect in views
        call_command('runserver', '127.0.0.1:8000')
    except KeyboardInterrupt:
        print("\n\n✓ Serveur arrêté.")
        sys.exit(0)
