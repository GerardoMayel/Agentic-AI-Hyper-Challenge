#!/usr/bin/env python3
"""
Sync data from Render PostgreSQL to local SQLite database
This script reads data from Render and creates a local SQLite copy for fallback
"""

import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.database import RENDER_DATABASE_URL, SQLITE_DATABASE_PATH, Base
from app.models.claim_models import ClaimForm, Document
from app.models.email_models import Email, ClaimSubmission, DocumentAgentOCR, DashboardStats, ClaimStatusUpdate

def create_sqlite_engine():
    """Create SQLite engine"""
    sqlite_url = f"sqlite:///{SQLITE_DATABASE_PATH}"
    return create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_render_engine():
    """Create Render PostgreSQL engine"""
    if not RENDER_DATABASE_URL:
        raise ValueError("RENDER_DATABASE_URL not found in environment")
    
    render_url = RENDER_DATABASE_URL
    if render_url.startswith("postgres://"):
        render_url = render_url.replace("postgres://", "postgresql://", 1)
    
    return create_engine(
        render_url,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 30}
    )

def sync_table_data(render_engine, sqlite_engine, table_name, query, transform_func=None):
    """Sync data from Render to SQLite for a specific table"""
    print(f"🔄 Syncing {table_name}...")
    
    try:
        # Read from Render
        with render_engine.connect() as conn:
            result = conn.execute(text(query))
            render_data = [dict(row._mapping) for row in result]
        
        print(f"   📊 Found {len(render_data)} records in Render")
        
        if not render_data:
            print(f"   ⏭️ No data to sync for {table_name}")
            return 0
        
        # Transform data if needed
        if transform_func:
            render_data = [transform_func(row) for row in render_data]
        
        # Write to SQLite
        with sqlite_engine.connect() as conn:
            # Clear existing data
            conn.execute(text(f"DELETE FROM {table_name}"))
            conn.commit()
            
            # Insert new data
            for i, row in enumerate(render_data):
                # Convert datetime objects to strings for SQLite
                for key, value in row.items():
                    if hasattr(value, 'isoformat'):
                        row[key] = value.isoformat()
                
                # Build INSERT statement
                columns = ', '.join(row.keys())
                placeholders = ', '.join([':' + key for key in row.keys()])
                insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                
                conn.execute(text(insert_query), row)
                
                if (i + 1) % 100 == 0:
                    print(f"   📝 Inserted {i + 1}/{len(render_data)} records")
            
            conn.commit()
        
        print(f"   ✅ Synced {len(render_data)} records to SQLite")
        return len(render_data)
        
    except Exception as e:
        print(f"   ❌ Error syncing {table_name}: {e}")
        return 0

def sync_claims_data(render_engine, sqlite_engine):
    """Sync claims data"""
    query = """
    SELECT 
        id, claim_number, customer_name, customer_email, policy_number,
        claim_type, incident_description, estimated_amount, status, priority,
        llm_summary, llm_recommendation, email_id, created_at, updated_at, closed_at
    FROM claim_submissions
    ORDER BY created_at DESC
    """
    
    return sync_table_data(render_engine, sqlite_engine, "claim_submissions", query)

def sync_emails_data(render_engine, sqlite_engine):
    """Sync emails data"""
    query = """
    SELECT 
        id, gmail_id, thread_id, from_email, to_email, subject, body_text,
        is_processed, is_first_notification, received_at, processed_at
    FROM emails
    ORDER BY received_at DESC
    """
    
    return sync_table_data(render_engine, sqlite_engine, "emails", query)

def sync_documents_data(render_engine, sqlite_engine):
    """Sync documents data"""
    query = """
    SELECT 
        id, claim_submission_id, original_filename, file_type, file_size,
        document_type, storage_url, is_processed, uploaded_at, processed_at,
        ocr_text, structured_data, inferred_costs
    FROM document_agent_ocr
    ORDER BY uploaded_at DESC
    """
    
    return sync_table_data(render_engine, sqlite_engine, "document_agent_ocr", query)

def sync_dashboard_stats(render_engine, sqlite_engine):
    """Sync dashboard stats"""
    query = """
    SELECT 
        id, total_claims, pending_claims, approved_claims, rejected_claims,
        closed_claims, total_amount_requested, total_amount_approved, last_updated
    FROM dashboard_stats
    ORDER BY last_updated DESC
    LIMIT 1
    """
    
    return sync_table_data(render_engine, sqlite_engine, "dashboard_stats", query)

def sync_status_updates(render_engine, sqlite_engine):
    """Sync status updates"""
    query = """
    SELECT 
        id, claim_submission_id, old_status, new_status, reason,
        analyst_name, created_at
    FROM claim_status_updates
    ORDER BY created_at DESC
    """
    
    return sync_table_data(render_engine, sqlite_engine, "claim_status_updates", query)

def create_sqlite_tables(sqlite_engine):
    """Create SQLite tables if they don't exist"""
    print("🔨 Creating SQLite tables...")
    
    try:
        Base.metadata.create_all(bind=sqlite_engine)
        print("✅ SQLite tables created/verified")
    except Exception as e:
        print(f"❌ Error creating SQLite tables: {e}")
        raise

def main():
    """Main sync function"""
    print("🔄 RENDER TO SQLITE SYNC")
    print("=" * 50)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Test Render connection
        print("\n🔍 Testing Render connection...")
        render_engine = create_render_engine()
        with render_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Render database is accessible")
        
        # Create SQLite engine and tables
        print("\n🔨 Setting up SQLite...")
        sqlite_engine = create_sqlite_engine()
        create_sqlite_tables(sqlite_engine)
        
        # Sync data
        print("\n📊 Starting data sync...")
        total_synced = 0
        
        # Sync each table
        total_synced += sync_claims_data(render_engine, sqlite_engine)
        total_synced += sync_emails_data(render_engine, sqlite_engine)
        total_synced += sync_documents_data(render_engine, sqlite_engine)
        total_synced += sync_dashboard_stats(render_engine, sqlite_engine)
        total_synced += sync_status_updates(render_engine, sqlite_engine)
        
        # Summary
        print("\n" + "=" * 50)
        print("🎉 SYNC COMPLETED")
        print(f"Total records synced: {total_synced}")
        print(f"SQLite database: {SQLITE_DATABASE_PATH}")
        print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Save sync metadata
        sync_info = {
            "last_sync": datetime.now().isoformat(),
            "total_records": total_synced,
            "sqlite_path": SQLITE_DATABASE_PATH,
            "render_url": RENDER_DATABASE_URL[:50] + "..." if RENDER_DATABASE_URL else None
        }
        
        metadata_path = os.path.join(os.path.dirname(SQLITE_DATABASE_PATH), "sync_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(sync_info, f, indent=2)
        
        print(f"Sync metadata saved to: {metadata_path}")
        
    except Exception as e:
        print(f"\n❌ Sync failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 