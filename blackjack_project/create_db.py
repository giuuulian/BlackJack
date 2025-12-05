#!/usr/bin/env python
"""
Script to create MySQL database
"""
import mysql.connector
import sys

def create_database():
    """Create the blackjack database"""
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            port=3306
        )
        
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS blackjack CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print("✓ Base de données 'blackjack' créée")
        
        cursor.close()
        conn.close()
        return True
    
    except mysql.connector.Error as err:
        print(f"✗ Erreur MySQL: {err}")
        print("\nVérifications:")
        print("1. MySQL/WAMP est démarré (Check phpMyAdmin)")
        print("2. Host: 127.0.0.1:3306")
        print("3. User: root")
        print("4. Password: vide (ou à configurer dans .env)")
        return False
    except Exception as e:
        print(f"✗ Erreur: {e}")
        return False

if __name__ == '__main__':
    success = create_database()
    sys.exit(0 if success else 1)
