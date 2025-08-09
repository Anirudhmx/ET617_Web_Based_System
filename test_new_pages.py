#!/usr/bin/env python3
"""
Test script for the new video lectures and text lessons pages
"""

import requests
from urllib.parse import urljoin

BASE_URL = "http://localhost:5000"

def test_home_page():
    """Test the home page loads correctly"""
    print("1. Testing home page...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("   ✅ Home page loads successfully")
            if "EduLearn" in response.text:
                print("   ✅ Home page content verified")
            else:
                print("   ⚠️  Home page content may be incomplete")
        else:
            print(f"   ❌ Home page failed to load: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Home page error: {e}")

def test_login_page():
    """Test the login page loads correctly"""
    print("\n2. Testing login page...")
    try:
        response = requests.get(f"{BASE_URL}/login")
        if response.status_code == 200:
            print("   ✅ Login page loads successfully")
            if "Login" in response.text:
                print("   ✅ Login page content verified")
            else:
                print("   ⚠️  Login page content may be incomplete")
        else:
            print(f"   ❌ Login page failed to load: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Login page error: {e}")

def test_video_lectures_page():
    """Test the video lectures page (should redirect to login when not authenticated)"""
    print("\n3. Testing video lectures page...")
    try:
        response = requests.get(f"{BASE_URL}/video_lectures", allow_redirects=False)
        if response.status_code == 302:  # Redirect to login
            print("   ✅ Video lectures page redirects to login (expected for unauthenticated users)")
        elif response.status_code == 200:
            print("   ✅ Video lectures page loads successfully")
            if "Video Lectures" in response.text:
                print("   ✅ Video lectures page content verified")
            else:
                print("   ⚠️  Video lectures page content may be incomplete")
        else:
            print(f"   ❌ Video lectures page failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Video lectures page error: {e}")

def test_text_lessons_page():
    """Test the text lessons page (should redirect to login when not authenticated)"""
    print("\n4. Testing text lessons page...")
    try:
        response = requests.get(f"{BASE_URL}/text_lessons", allow_redirects=False)
        if response.status_code == 302:  # Redirect to login
            print("   ✅ Text lessons page redirects to login (expected for unauthenticated users)")
        elif response.status_code == 200:
            print("   ✅ Text lessons page loads successfully")
            if "Text Lessons" in response.text:
                print("   ✅ Text lessons page content verified")
            else:
                print("   ⚠️  Text lessons page content may be incomplete")
        else:
            print(f"   ❌ Text lessons page failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Text lessons page error: {e}")

def test_navigation_links():
    """Test that navigation links are present on the home page"""
    print("\n5. Testing navigation links...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            if "Video Lectures" in response.text and "Text Lessons" in response.text:
                print("   ✅ Navigation links for new pages found on home page")
            else:
                print("   ⚠️  Navigation links may not be visible to unauthenticated users")
        else:
            print(f"   ❌ Cannot test navigation links: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Navigation test error: {e}")

def main():
    """Run all tests"""
    print("=" * 50)
    print("Testing New Pages: Video Lectures & Text Lessons")
    print("=" * 50)
    
    test_home_page()
    test_login_page()
    test_video_lectures_page()
    test_text_lessons_page()
    test_navigation_links()
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("- Home page should load with EduLearn content")
    print("- Login page should be accessible")
    print("- Video lectures page should redirect to login (unauthenticated)")
    print("- Text lessons page should redirect to login (unauthenticated)")
    print("- Navigation should include new page links")
    print("\nNote: New pages require authentication to access content.")
    print("=" * 50)

if __name__ == "__main__":
    main()
