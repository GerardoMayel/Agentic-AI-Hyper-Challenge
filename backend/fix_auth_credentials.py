#!/usr/bin/env python3
"""
Script para verificar y corregir credenciales de autenticación
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.database import engine
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
import time

def create_auth_table():
    """Create auth_credentials table if it doesn't exist"""
    try:
        with engine.connect() as conn:
            # Check if table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'auth_credentials'
                );
            """))
            
            table_exists_result = result.fetchone()
            if table_exists_result:
                table_exists = table_exists_result[0]
            else:
                table_exists = False
            
            if not table_exists:
                print("🔨 Creating auth_credentials table...")
                conn.execute(text("""
                    CREATE TABLE auth_credentials (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        role VARCHAR(50) DEFAULT 'analyst',
                        is_active BOOLEAN DEFAULT true,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """))
                conn.commit()
                print("✅ auth_credentials table created")
            else:
                print("✅ auth_credentials table already exists")
                
        return True
        
    except Exception as e:
        print(f"❌ Error creating auth table: {e}")
        return False

def insert_demo_credentials():
    """Insert demo credentials"""
    try:
        with engine.connect() as conn:
            # Check if credentials already exist
            result = conn.execute(text("""
                SELECT COUNT(*) FROM auth_credentials WHERE email = 'analyst@zurich-demo.com'
            """))
            
            count_result = result.fetchone()
            if count_result:
                count = count_result[0]
            else:
                count = 0
            
            if count == 0:
                print("🔑 Inserting demo credentials...")
                conn.execute(text("""
                    INSERT INTO auth_credentials (email, password_hash, role, is_active)
                    VALUES ('analyst@zurich-demo.com', 'ZurichDemo2024!', 'analyst', true)
                    ON CONFLICT (email) DO NOTHING;
                """))
                conn.commit()
                print("✅ Demo credentials inserted")
            else:
                print("✅ Demo credentials already exist")
                
        return True
        
    except Exception as e:
        print(f"❌ Error inserting credentials: {e}")
        return False

def verify_credentials():
    """Verify that credentials work"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT email, password_hash, role, is_active 
                FROM auth_credentials 
                WHERE is_active = true
            """))
            
            credentials = result.fetchall()
            
            if credentials:
                print("✅ Credentials found:")
                for cred in credentials:
                    print(f"   - Email: {cred[0]}")
                    print(f"   - Role: {cred[2]}")
                    print(f"   - Active: {cred[3]}")
                return True
            else:
                print("❌ No active credentials found")
                return False
                
    except Exception as e:
        print(f"❌ Error verifying credentials: {e}")
        return False

def test_login():
    """Test login functionality"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT email, password_hash, role 
                FROM auth_credentials 
                WHERE email = 'analyst@zurich-demo.com' AND is_active = true
            """))
            
            cred = result.fetchone()
            
            if cred:
                email, password_hash, role = cred
                print(f"✅ Login test successful:")
                print(f"   - Email: {email}")
                print(f"   - Password matches: {'ZurichDemo2024!' == password_hash}")
                print(f"   - Role: {role}")
                return True
            else:
                print("❌ Login test failed - credentials not found")
                return False
                
    except Exception as e:
        print(f"❌ Error testing login: {e}")
        return False

def main():
    """Main function"""
    print("🔐 AUTH CREDENTIALS SETUP")
    print("=" * 50)
    
    # Test database connection with retry
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print("✅ Database connection successful")
                break
        except OperationalError as e:
            if "SSL connection has been closed" in str(e) and attempt < max_retries - 1:
                print(f"⚠️  SSL connection error, retrying... (attempt {attempt + 1}/{max_retries})")
                time.sleep(2)
                continue
            else:
                print(f"❌ Database connection failed: {e}")
                return False
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    # Create table
    if not create_auth_table():
        return False
    
    # Insert credentials
    if not insert_demo_credentials():
        return False
    
    # Verify credentials
    if not verify_credentials():
        return False
    
    # Test login
    if not test_login():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 AUTH CREDENTIALS SETUP COMPLETE!")
    print("✅ Login should now work with:")
    print("   - Email: analyst@zurich-demo.com")
    print("   - Password: ZurichDemo2024!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 