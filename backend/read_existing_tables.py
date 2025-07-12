"""
Read existing tables from database
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import text, create_engine, inspect

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def read_existing_tables():
    """Read and display existing tables in the database"""
    print("🔍 Reading existing tables from database...")
    
    # Load environment variables
    load_dotenv()
    
    # Get DATABASE_URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    print(f"✅ Using DATABASE_URL: {database_url[:50]}...")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
            print("✅ Database connection successful!")
            
            # Get database name
            result = connection.execute(text("SELECT current_database()"))
            db_row = result.fetchone()
            if db_row:
                db_name = db_row[0]
                print(f"✅ Connected to database: {db_name}")
            
            # Get inspector
            inspector = inspect(engine)
            
            # Get all tables
            tables = inspector.get_table_names()
            
            print(f"\n📋 Tables found in database: {len(tables)}")
            
            if not tables:
                print("  📭 No tables found - database is empty")
            else:
                print("  📊 Existing tables:")
                for i, table_name in enumerate(tables, 1):
                    print(f"    {i}. {table_name}")
                    
                    # Get columns for each table
                    columns = inspector.get_columns(table_name)
                    print(f"       Columns ({len(columns)}):")
                    for column in columns:
                        nullable = "NULL" if column['nullable'] else "NOT NULL"
                        print(f"         - {column['name']}: {column['type']} {nullable}")
                    
                    # Get indexes
                    indexes = inspector.get_indexes(table_name)
                    if indexes:
                        print(f"       Indexes ({len(indexes)}):")
                        for index in indexes:
                            unique = "UNIQUE" if index['unique'] else ""
                            column_names = [name for name in index['column_names'] if name is not None]
                            print(f"         - {index['name']}: {', '.join(column_names)} {unique}")
                    
                    print()  # Empty line between tables
            
            return True
            
    except Exception as e:
        print(f"❌ Error reading tables: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Database Tables Reader")
    print("=" * 50)
    
    if read_existing_tables():
        print("\n✅ Table reading completed successfully!")
    else:
        print("\n❌ Failed to read tables")
        sys.exit(1) 