#!/usr/bin/env python
"""
Script to generate HTTPS certificates for local development
Uses cryptography library instead of openssl
"""
import os
import sys
from datetime import datetime, timedelta

def generate_certificates_with_cryptography():
    """Generate self-signed certificates using cryptography library"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
    except ImportError:
        print("✗ Module 'cryptography' non trouvé.")
        print("  Installation: pip install cryptography")
        return False
    
    cert_dir = 'certs'
    os.makedirs(cert_dir, exist_ok=True)
    
    cert_file = os.path.join(cert_dir, 'localhost.crt')
    key_file = os.path.join(cert_dir, 'localhost.key')
    
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print("✓ Certificats HTTPS déjà présents")
        return True
    
    print("Génération des certificats HTTPS auto-signés...")
    
    try:
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        # Generate certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(u"localhost"),
                x509.DNSName(u"127.0.0.1"),
                x509.DNSName(u"*.localhost"),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256(), default_backend())
        
        # Write certificate to file
        with open(cert_file, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        # Write private key to file
        with open(key_file, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print(f"✓ Certificats générés avec succès:")
        print(f"  - {cert_file}")
        print(f"  - {key_file}")
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors de la génération: {e}")
        return False

if __name__ == '__main__':
    success = generate_certificates_with_cryptography()
    sys.exit(0 if success else 1)
