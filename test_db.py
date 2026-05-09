from app import app, db

# IMPORTANT: Import models BEFORE creating tables
from models.user import User
from models.task import Task

def test_connection():
    with app.app_context():
        try:
            # Test connection
            result = db.engine.connect()
            print("✅ Database connection successful!")
            
            # Import models to register them with SQLAlchemy
            print("Importing models...")
            from models.user import User
            from models.task import Task
            
            # Create all tables
            print("Creating tables...")
            db.create_all()
            print("✅ Create tables command executed!")
            
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Tables in database: {tables}")
            
            if tables:
                print("✅ Tables created successfully!")
            else:
                print("❌ Still no tables. Let me try something else...")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_connection()