import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base
from app.models.users import User
from app.utils.auth import hash_password, pwd_context

# Load environment variables
load_dotenv()

def get_db_session():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("Error: DATABASE_URL environment variable not set")
        return None
    
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal()
    except Exception as e:
        print(f"Error creating database session: {str(e)}")
        return None

def update_passwords():
    db = get_db_session()
    if not db:
        return

    try:
        # Get all users
        users = db.query(User).all()
        if not users:
            print("No users found in the database.")
            return

        updated_count = 0
        for user in users:
            if not user.password_hash:
                print(f"Skipping user {user.email}: No password hash")
                continue
                
            # Check if the password is already hashed with bcrypt-sha256
            if user.password_hash.startswith("$bcrypt-sha256$"):
                print(f"Skipping user {user.email}: Already using bcrypt-sha256")
                continue
                
            print(f"Updating password for user: {user.email}")
            
            try:
                # If the password is not already hashed with bcrypt-sha256, hash it
                user.password_hash = hash_password(user.password_hash)
                db.commit()
                updated_count += 1
                print(f"Successfully updated password for {user.email}")
            except Exception as e:
                db.rollback()
                print(f"Error updating password for {user.email}: {str(e)}")

        print(f"\nPassword update completed! Updated {updated_count} users.")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if db:
            db.close()

if __name__ == "__main__":
    print("Starting password update process...")
    update_passwords()
