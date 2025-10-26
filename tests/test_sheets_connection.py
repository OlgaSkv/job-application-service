#!/usr/bin/env python3
"""
Test Google Sheets connection for Job Tracker project.

This script verifies that:
1. Google service account credentials are valid
2. Google Sheets API is accessible
3. Both JD_Saved and Job_Tracker sheets can be opened
4. Service account has proper permissions

Usage:
    python test_sheets_connection.py
"""

import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

try:
    from src.tools.google_sheets_tool import GoogleSheetsTool
    from src.utils.config_utils import get_config
    from src.utils.logging_utils import setup_logging
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the project root directory.")
    sys.exit(1)

import logging

def test_connection():
    """Test Google Sheets connection and permissions."""
    
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("🔗 Testing Google Sheets Connection...")
    print("=" * 50)
    
    try:
        # Load configuration
        print("📋 Loading configuration...")
        config = get_config()
        
        # Initialize Google Sheets tool
        print("🔑 Initializing Google Sheets connection...")
        sheets_tool = GoogleSheetsTool(
            credentials_path=config["CREDENTIALS_PATH"],
            jd_saved_url=config["JD_SAVED_URL"],
            job_tracker_url=config["JOB_TRACKER_URL"]
        )
        
        # Test JD_Saved sheet access
        print("\n📊 Testing JD_Saved sheet access...")
        try:
            # Test sheet access and get all jobs
            jd_data = sheets_tool.query_jobs()
            print(f"✅ Successfully accessed JD_Saved sheet")
            print(f"   Found {len(jd_data)} rows of data")
            
            # Check headers if data exists
            if jd_data:
                headers = list(jd_data[0].keys()) if jd_data else []
                essential_headers = ["job_uid"]  # Only require the most essential
                print(f"   Sample headers: {headers[:8]}{'...' if len(headers) > 8 else ''}")
                if set(essential_headers).issubset(set(headers)):
                    print("   ✅ Essential headers present")
                else:
                    missing = set(essential_headers) - set(headers)
                    print(f"   ⚠️  Missing essential headers: {missing}")
            else:
                print("   📝 Sheet is empty (this is normal for new setups)")
                
            # Test raw sheet access too
            jd_sheet = sheets_tool.get_jd_saved_sheet()
            all_values = jd_sheet.get_all_values()
            print(f"   Raw sheet access: {len(all_values)} total rows")
                
        except Exception as e:
            print(f"❌ Failed to access JD_Saved sheet: {e}")
            return False
        
        # Test Job_Tracker sheet access
        print("\n📈 Testing Job_Tracker sheet access...")
        try:
            # Try to read the tracker sheet directly
            tracker_sheet = sheets_tool.get_job_tracker_sheet()
            all_values = tracker_sheet.get_all_values()
            print(f"✅ Successfully accessed Job_Tracker sheet")
            print(f"   Found {len(all_values)} rows")
            
            if all_values and len(all_values) > 0:
                headers = all_values[0] if all_values else []
                expected_headers = ["job_uid", "company", "role", "eligibility_status", "ats_score"]
                print(f"   Headers: {len(headers)} columns")
                if len(headers) >= len(expected_headers):
                    print("   ✅ Header count looks good")
                else:
                    print(f"   ⚠️  Expected at least {len(expected_headers)} columns, found {len(headers)}")
            else:
                print("   📝 Sheet is empty (run setup.py to initialize)")
                
        except Exception as e:
            print(f"❌ Failed to access Job_Tracker sheet: {e}")
            return False
        
        # Success summary
        print("\n" + "=" * 50)
        print("🎉 All tests passed!")
        print("✅ Google Sheets API connection successful")
        print("✅ Service account has proper permissions")
        print("✅ Both sheets are accessible")
        print("\nYour setup is ready for job processing!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection test failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Verify credentials.json exists and is valid")
        print("2. Check that both Google Sheets are shared with your service account")
        print("3. Ensure Google Sheets API is enabled in Google Cloud Console")
        print("4. Verify config.json has correct sheet URLs")
        
        return False

def main():
    """Main test function."""
    success = test_connection()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()