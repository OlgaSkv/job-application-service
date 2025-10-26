#!/usr/bin/env python3
"""
Test Google Drive connection for Job Tracker project.

This script verifies that:
1. Google service account credentials are valid
2. Google Drive API is accessible
3. Service account can access configured files (resume, statement, profile)
4. Files can be downloaded and read successfully

Usage:
    python tests/test_drive_connection.py
"""

import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

try:
    from src.tools.google_drive_tool import GoogleDriveTool
    from src.utils.config_utils import get_config
    from src.utils.logging_utils import setup_logging
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the project root directory.")
    sys.exit(1)

import logging

def test_drive_connection():
    """Test Google Drive connection and file access."""
    
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("🔗 Testing Google Drive Connection...")
    print("=" * 50)
    
    try:
        # Load configuration
        print("📋 Loading configuration...")
        config = get_config()
        
        # Initialize Google Drive tool
        print("🔑 Initializing Google Drive connection...")
        drive_tool = GoogleDriveTool(credentials_path=config["CREDENTIALS_PATH"])
        
        # Test basic Drive API access
        print("\n📁 Testing Google Drive API access...")
        try:
            # Test basic API connectivity with a simple files list
            files_result = drive_tool.service.files().list(
                pageSize=5,
                fields="files(id, name, mimeType)"
            ).execute()
            files = files_result.get('files', [])
            print(f"✅ Successfully connected to Google Drive API")
            print(f"   Can see {len(files)} files (showing max 5 for test)")
            
        except Exception as e:
            print(f"❌ Failed to access Google Drive API: {e}")
            return False
        
        # Test configured file access
        print("\n📄 Testing configured file access...")
        
        test_files = []
        
        # Resume file
        if "RESUME_FILE_ID" in config:
            test_files.append(("Resume", config["RESUME_FILE_ID"], "resume content"))
        
        # Statement file  
        if "STATEMENT_FILE_ID" in config:
            test_files.append(("Personal Statement", config["STATEMENT_FILE_ID"], "statement content"))
        
        success_count = 0
        total_files = len(test_files)
        
        for file_name, file_id, content_type in test_files:
            print(f"\n🔍 Testing {file_name}...")
            print(f"   File ID: {file_id}")
            
            try:
                # Test file metadata access
                file_metadata = drive_tool.service.files().get(fileId=file_id).execute()
                print(f"   ✅ File metadata accessible")
                print(f"   Name: {file_metadata.get('name', 'Unknown')}")
                print(f"   Type: {file_metadata.get('mimeType', 'Unknown')}")
                
                # Test file content access
                content = drive_tool.load_doc(file_id)
                if content:
                    content_preview = content[:100].replace('\n', ' ').strip()
                    print(f"   ✅ File content loaded ({len(content)} characters)")
                    print(f"   Preview: {content_preview}...")
                    success_count += 1
                else:
                    print(f"   ⚠️  File metadata accessible but content is empty")
                    
            except Exception as e:
                print(f"   ❌ Failed to access {file_name}: {e}")
                print(f"   This file may not be shared with your service account")
        
        # Test profile file (local file)
        print(f"\n📊 Testing local profile file...")
        profile_path = config.get("PROFILE_FILE_PATH", "data/candidate_profile.json")
        full_profile_path = os.path.join(project_root, profile_path)
        
        if os.path.exists(full_profile_path):
            try:
                with open(full_profile_path, 'r', encoding='utf-8') as f:
                    profile_content = f.read()
                print(f"   ✅ Profile file accessible")
                print(f"   Path: {profile_path}")
                print(f"   Size: {len(profile_content)} characters")
            except Exception as e:
                print(f"   ❌ Failed to read profile file: {e}")
        else:
            print(f"   ⚠️  Profile file not found at: {profile_path}")
            print(f"   Full path: {full_profile_path}")
        
        # Summary
        print("\n" + "=" * 50)
        
        if success_count == total_files and total_files > 0:
            print("🎉 All tests passed!")
            print("✅ Google Drive API connection successful")
            print("✅ Service account has proper file permissions")
            print(f"✅ All {total_files} configured files accessible")
            print("\nYour Google Drive setup is ready for job processing!")
            return True
        elif success_count > 0:
            print("⚠️  Partial success")
            print("✅ Google Drive API connection successful")
            print(f"✅ {success_count}/{total_files} files accessible")
            print(f"⚠️  {total_files - success_count} files need permission fixes")
            print("\nSome files may need to be shared with your service account.")
            return True
        else:
            print("❌ Connection issues detected")
            print("✅ Google Drive API connection successful")
            print("❌ No configured files are accessible")
            print("\nAll files need to be shared with your service account.")
            return False
        
    except Exception as e:
        print(f"\n❌ Drive connection test failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Verify credentials.json exists and is valid")
        print("2. Check that Google Drive API is enabled in Google Cloud Console")
        print("3. Ensure all files are shared with your service account email")
        print("4. Verify file IDs in config.json are correct")
        print("5. Check that service account has 'Viewer' permission on shared files")
        
        return False

def get_service_account_email():
    """Extract service account email from credentials for reference."""
    try:
        config = get_config()
        credentials_path = config["CREDENTIALS_PATH"]
        
        if os.path.exists(credentials_path):
            import json
            with open(credentials_path, 'r') as f:
                creds = json.load(f)
                return creds.get('client_email', 'Unknown')
        return 'Credentials file not found'
    except Exception:
        return 'Error reading credentials'

def main():
    """Main test function."""
    print("Google Drive Connection Test")
    print("Job Tracker Project")
    print("")
    
    # Show service account email for reference
    email = get_service_account_email()
    print(f"Service Account: {email}")
    print("Share your Google Drive files with this email address.")
    print("")
    
    success = test_drive_connection()
    
    if not success:
        print("\n" + "=" * 50)
        print("SETUP HELP:")
        print("To fix file access issues:")
        print("1. Open each file in Google Drive")
        print("2. Click the 'Share' button")
        print(f"3. Add this email: {email}")
        print("4. Set permission to 'Viewer'")
        print("5. Click 'Send' or 'Done'")
        print("6. Run this test again")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()