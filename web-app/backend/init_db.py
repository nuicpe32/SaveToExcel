"""
Database Initialization Script
Creates all tables defined in SQLAlchemy models
"""

from app.core.database import engine, Base
from app.models.user import User
from app.models.bank_account import BankAccount
from app.models.suspect import Suspect
from app.models.criminal_case import CriminalCase
from app.models.post_arrest import PostArrest

def init_database():
    """Initialize database by creating all tables"""
    try:
        print("🔄 Creating database tables...")

        # Import all models to ensure they are registered with Base
        # (Already imported above)

        # Create all tables
        Base.metadata.create_all(bind=engine)

        print("✅ Database tables created successfully!")
        print("\nCreated tables:")
        print("  - users")
        print("  - bank_accounts")
        print("  - suspects")
        print("  - criminal_cases")
        print("  - post_arrests")
        print("\n📝 Next step: Run 'python create_admin.py' to create admin user")

    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise

if __name__ == "__main__":
    init_database()