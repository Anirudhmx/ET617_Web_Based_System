#!/usr/bin/env python3
"""
Admin User Management Script for ET617 Learning Platform
This script helps manage admin users and their privileges
"""

import os
import sys
from main import app, db, User
from werkzeug.security import generate_password_hash

def create_admin_user(username, email, password):
    """Create a new admin user"""
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"❌ User '{username}' already exists!")
            return False
        
        # Create new admin user
        admin_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_student=False,
            is_admin=True
        )
        
        db.session.add(admin_user)
        db.session.commit()
        
        print(f"✅ Admin user '{username}' created successfully!")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"   Admin: Yes")
        return True

def make_user_admin(username):
    """Make an existing user an admin"""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"❌ User '{username}' not found!")
            return False
        
        user.is_admin = True
        user.is_student = False
        db.session.commit()
        
        print(f"✅ User '{username}' is now an admin!")
        return True

def list_admin_users():
    """List all admin users"""
    with app.app_context():
        admin_users = User.query.filter_by(is_admin=True).all()
        
        if not admin_users:
            print("ℹ️ No admin users found.")
            return
        
        print("👑 Admin Users:")
        print("-" * 50)
        for user in admin_users:
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Created: {user.created_at}")
            print(f"Student: {user.is_student}")
            print("-" * 50)

def list_all_users():
    """List all users"""
    with app.app_context():
        users = User.query.all()
        
        if not users:
            print("ℹ️ No users found.")
            return
        
        print("👥 All Users:")
        print("-" * 50)
        for user in users:
            admin_badge = "👑" if user.is_admin else ""
            student_badge = "🎓" if user.is_student else "👨‍🏫"
            print(f"{admin_badge} {student_badge} {user.username} ({user.email})")
            print(f"   Admin: {user.is_admin}, Student: {user.is_student}")
            print("-" * 50)

def main():
    print("🔐 ET617 Learning Platform - Admin Manager")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python admin_manager.py create <username> <email> <password>")
        print("  python admin_manager.py make-admin <username>")
        print("  python admin_manager.py list-admins")
        print("  python admin_manager.py list-users")
        print("\nExamples:")
        print("  python admin_manager.py create admin admin@example.com admin123")
        print("  python admin_manager.py make-admin john")
        print("  python admin_manager.py list-admins")
        return
    
    command = sys.argv[1].lower()
    
    if command == "create" and len(sys.argv) == 5:
        username = sys.argv[2]
        email = sys.argv[3]
        password = sys.argv[4]
        create_admin_user(username, email, password)
    
    elif command == "make-admin" and len(sys.argv) == 3:
        username = sys.argv[2]
        make_user_admin(username)
    
    elif command == "list-admins":
        list_admin_users()
    
    elif command == "list-users":
        list_all_users()
    
    else:
        print("❌ Invalid command or arguments!")
        print("Use 'python admin_manager.py' for help.")

if __name__ == "__main__":
    main()
