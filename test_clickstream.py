#!/usr/bin/env python3
"""
Test script for clickstream functionality
This script demonstrates how to test the clickstream tracking system
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpass123"

def test_clickstream_functionality():
    """Test the complete clickstream functionality"""
    
    print("🚀 Testing Clickstream Functionality")
    print("=" * 50)
    
    # Test 1: Track anonymous clicks
    print("\n1. Testing anonymous click tracking...")
    test_anonymous_clicks()
    
    # Test 2: User registration and login
    print("\n2. Testing user authentication...")
    session = test_user_auth()
    
    if session:
        # Test 3: Track authenticated user clicks
        print("\n3. Testing authenticated user click tracking...")
        test_authenticated_clicks(session)
        
        # Test 4: Test export page access
        print("\n4. Testing export page access...")
        test_export_page_access(session)
        
        # Test 5: Test Excel export
        print("\n5. Testing Excel export...")
        test_excel_export(session)
    
    print("\n✅ Clickstream testing completed!")

def test_anonymous_clicks():
    """Test tracking clicks from anonymous users"""
    
    # Simulate various click events
    click_events = [
        {
            "page_url": f"{BASE_URL}/",
            "element_id": "hero-section",
            "element_class": "hero-section",
            "element_text": "Welcome to EduLearn",
            "click_x": 150,
            "click_y": 200
        },
        {
            "page_url": f"{BASE_URL}/",
            "element_id": "courses-section",
            "element_class": "card course-card",
            "element_text": "View Course",
            "click_x": 300,
            "click_y": 400
        }
    ]
    
    for i, event in enumerate(click_events, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/track_click",
                json=event,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"   ✅ Anonymous click {i} tracked successfully")
            else:
                print(f"   ❌ Anonymous click {i} failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Anonymous click {i} error: {e}")
        
        time.sleep(0.5)  # Small delay between requests

def test_user_auth():
    """Test user registration and login"""
    
    # Register new user
    try:
        register_data = {
            "username": TEST_USERNAME,
            "email": f"{TEST_USERNAME}@example.com",
            "password": TEST_PASSWORD
        }
        
        response = requests.post(f"{BASE_URL}/register", data=register_data)
        
        if response.status_code == 200:
            print("   ✅ User registration successful")
        else:
            print(f"   ⚠️  User registration status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ User registration error: {e}")
    
    # Login
    try:
        login_data = {
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD
        }
        
        response = requests.post(f"{BASE_URL}/login", data=login_data, allow_redirects=False)
        
        if response.status_code == 302:  # Redirect after successful login
            print("   ✅ User login successful")
            
            # Get session cookies
            session = requests.Session()
            session.cookies.update(response.cookies)
            return session
        else:
            print(f"   ❌ User login failed: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ User login error: {e}")
        return None

def test_authenticated_clicks(session):
    """Test tracking clicks from authenticated users"""
    
    # Simulate authenticated user interactions
    auth_events = [
        {
            "page_url": f"{BASE_URL}/course/1",
            "element_id": "lecture-tab",
            "element_class": "nav-link",
            "element_text": "Lectures",
            "click_x": 100,
            "click_y": 150
        },
        {
            "page_url": f"{BASE_URL}/course/1",
            "element_id": "notes-tab",
            "element_class": "nav-link",
            "element_text": "Notes",
            "click_x": 200,
            "click_y": 150
        },
        {
            "page_url": f"{BASE_URL}/create_course",
            "element_id": "course-form",
            "element_class": "form",
            "element_text": "Create New Course",
            "click_x": 250,
            "click_y": 300
        }
    ]
    
    for i, event in enumerate(auth_events, 1):
        try:
            response = session.post(
                f"{BASE_URL}/track_click",
                json=event,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"   ✅ Authenticated click {i} tracked successfully")
            else:
                print(f"   ❌ Authenticated click {i} failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Authenticated click {i} error: {e}")
        
        time.sleep(0.5)

def test_export_page_access(session):
    """Test access to the export data page"""
    
    try:
        response = session.get(f"{BASE_URL}/export_data")
        
        if response.status_code == 200:
            print("   ✅ Export page access successful")
            
            # Check if export page contains expected content
            if "Export Clickstream Data" in response.text:
                print("   ✅ Export page content verified")
            else:
                print("   ⚠️  Export page content may be incomplete")
        else:
            print(f"   ❌ Export page access failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Export page access error: {e}")

def test_excel_export(session):
    """Test Excel export functionality"""
    
    try:
        response = session.get(f"{BASE_URL}/export_clickstream")
        
        if response.status_code == 200:
            print("   ✅ Excel export successful")
            
            # Check if response contains Excel content
            if response.headers.get('content-type', '').startswith('application/vnd.openxmlformats-officedocument'):
                print("   ✅ Excel file format verified")
                
                # Save the file for inspection
                filename = f"clickstream_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"   💾 Excel file saved as: {filename}")
            else:
                print("   ⚠️  Excel file format may be incorrect")
        else:
            print(f"   ❌ Excel export failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Excel export error: {e}")

def check_server_status():
    """Check if the Flask server is running"""
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and accessible")
            return True
        else:
            print(f"⚠️  Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Make sure the Flask application is running with: python main.py")
        return False

if __name__ == "__main__":
    print("🔍 Clickstream Testing Tool")
    print("=" * 50)
    
    # Check server status first
    if check_server_status():
        test_clickstream_functionality()
    else:
        print("\n❌ Please start the Flask server first:")
        print("   cd ET617_Web_Based_System")
        print("   python main.py")
        print("\nThen run this test script in another terminal.")
