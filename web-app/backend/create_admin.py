from app.core.security import get_password_hash
from app.core.database import get_db
from app.models.user import User, UserRole

def create_admin():
    db = next(get_db())
    try:
        # ตรวจสอบว่ามี admin อยู่แล้วหรือไม่
        existing_admin = db.query(User).filter(User.username == 'admin').first()
        if existing_admin:
            print("⚠️  Admin user already exists!")
            print("Username: admin")
            return

        # สร้าง admin user ใหม่
        admin = User(
            username='admin',
            email='admin@example.com',
            full_name='Administrator',
            hashed_password=get_password_hash('admin123'),
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("✅ Admin user created successfully!")
        print("=" * 50)
        print("Username: admin")
        print("Password: admin123")
        print("Email: admin@example.com")
        print("Role: ADMIN")
        print("=" * 50)
        print("\n🌐 You can now login at: http://localhost:3000")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()