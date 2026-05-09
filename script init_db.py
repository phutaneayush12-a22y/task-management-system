from app import app, db
from models.user import User
from models.task import Task

def init_database():
    with app.app_context():
        # Drop all tables (if they exist)
        db.drop_all()
        print("Dropped existing tables")
        
        # Create all tables
        db.create_all()
        print("Created all tables successfully!")
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Tables in database: {tables}")

if __name__ == "__main__":
    init_database()