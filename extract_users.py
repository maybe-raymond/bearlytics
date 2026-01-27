#!/usr/bin/env python3
"""
Script to extract usernames and password hashes from the Bearlytics database.

Note: Django stores passwords as one-way hashes (PBKDF2), so they cannot be
decrypted back to plain text. This script will show the stored password hashes.

Usage:
    python extract_users.py [SALT_SECRET]
    python extract_users.py [--db-path DB_PATH] [--salt-secret SALT_SECRET]

Environment Variables:
    DB_PATH: Path to SQLite database (default: /app/data/analytics.db)
    SALT_SECRET: Salt secret for reference (optional)
"""

import os
import sqlite3
import sys
import argparse
from pathlib import Path


def get_db_path():
    """Get database path from environment variable or use default."""
    db_path = os.getenv('DB_PATH', '/app/data/analytics.db')
    
    # If default path doesn't exist, try local development path
    if not os.path.exists(db_path):
        local_path = os.path.join(os.path.dirname(__file__), 'analytics', 'analytics.db')
        if os.path.exists(local_path):
            return local_path
    
    return db_path


def extract_users(db_path, salt_secret=None):
    """
    Extract usernames and password hashes from the database.
    
    Args:
        db_path: Path to the SQLite database file
        salt_secret: SALT_SECRET (optional, for reference only - not used for password decryption)
    """
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}", file=sys.stderr)
        print("Please ensure DB_PATH is set correctly or the database exists.", file=sys.stderr)
        sys.exit(1)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query the auth_user table (Django's default user table)
        cursor.execute("""
            SELECT 
                id,
                username,
                email,
                password,
                is_superuser,
                is_staff,
                is_active,
                date_joined,
                last_login
            FROM auth_user
            ORDER BY id
        """)
        
        users = cursor.fetchall()
        
        if not users:
            print("No users found in the database.")
            return
        
        print("=" * 80)
        print("USERS AND PASSWORD HASHES")
        print("=" * 80)
        if salt_secret:
            print(f"SALT_SECRET: {salt_secret}")
            print("-" * 80)
        print()
        
        for user in users:
            user_id, username, email, password_hash, is_superuser, is_staff, is_active, date_joined, last_login = user
            
            print(f"ID: {user_id}")
            print(f"Username: {username}")
            if email:
                print(f"Email: {email}")
            print(f"Password Hash: {password_hash}")
            print(f"Superuser: {is_superuser}")
            print(f"Staff: {is_staff}")
            print(f"Active: {is_active}")
            if date_joined:
                print(f"Date Joined: {date_joined}")
            if last_login:
                print(f"Last Login: {last_login}")
            print("-" * 80)
        
        conn.close()
        
        print()
        print("NOTE: Passwords are stored as one-way hashes (PBKDF2) and cannot be")
        print("decrypted. The password hash shown above can only be used to verify")
        print("passwords, not to recover the original password.")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Extract usernames and password hashes from Bearlytics database'
    )
    parser.add_argument(
        '--db-path',
        type=str,
        help='Path to SQLite database file (overrides DB_PATH env var)'
    )
    parser.add_argument(
        '--salt-secret',
        type=str,
        help='SALT_SECRET for reference (overrides SALT_SECRET env var)'
    )
    parser.add_argument(
        'salt_secret_pos',
        nargs='?',
        help='SALT_SECRET as positional argument (for convenience)'
    )
    
    args = parser.parse_args()
    
    # Get SALT_SECRET from command line, environment, or None
    salt_secret = args.salt_secret or args.salt_secret_pos or os.getenv('SALT_SECRET')
    
    # Get database path from command line or environment
    db_path = args.db_path or get_db_path()
    
    print(f"Database: {db_path}")
    print()
    
    # Extract and display users
    extract_users(db_path, salt_secret)


if __name__ == '__main__':
    main()
