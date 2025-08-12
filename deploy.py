#!/usr/bin/env python3
"""
Deployment Helper Script for ET617 Learning Platform
This script helps prepare your app for deployment
"""

import os
import secrets
import subprocess
import sys

def generate_secret_key():
    """Generate a secure secret key"""
    return secrets.token_hex(32)

def check_files():
    """Check if all required deployment files exist"""
    required_files = [
        'main.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required deployment files found")
    return True

def create_env_file():
    """Create a .env file with sample environment variables"""
    env_content = f"""# Environment variables for deployment
SECRET_KEY={generate_secret_key()}
DATABASE_URL=sqlite:///learning_platform.db
FLASK_ENV=production
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with sample environment variables")

def check_git_status():
    """Check git status and provide deployment commands"""
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository found")
            print("\n📋 Next steps for deployment:")
            print("1. Add and commit your changes:")
            print("   git add .")
            print("   git commit -m 'Prepare for deployment'")
            print("2. Push to GitHub:")
            print("   git push origin main")
            print("3. Deploy on Render/Railway following the DEPLOYMENT.md guide")
        else:
            print("❌ Git repository not found or not initialized")
            print("Initialize git with: git init")
    except FileNotFoundError:
        print("❌ Git not installed. Please install Git first.")

def main():
    print("🚀 ET617 Learning Platform - Deployment Helper")
    print("=" * 50)
    
    # Check required files
    if not check_files():
        print("\nPlease create the missing files before deploying.")
        return
    
    # Create environment file
    create_env_file()
    
    # Check git status
    check_git_status()
    
    print("\n📚 For detailed deployment instructions, see DEPLOYMENT.md")
    print("🎯 Recommended hosting: Render.com (free tier)")

if __name__ == "__main__":
    main()
