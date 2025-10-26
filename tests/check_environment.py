"""Quick environment validation script for Job Tracker."""
import sys
import os
from pathlib import Path

def check_environment():
    """Validate testing environment."""
    checks = []
    
    # Check Python version
    py_version = sys.version_info
    checks.append(("Python Version", py_version >= (3, 11), f"{py_version.major}.{py_version.minor}.{py_version.micro}"))
    
    # Check required files
    required_files = ['.env', 'config.json', 'credentials.json', 'data/candidate_profile.json']
    for file in required_files:
        exists = Path(file).exists()
        checks.append((f"File: {file}", exists, "Present" if exists else "Missing"))
    
    # Check required packages
    try:
        import langgraph
        try:
            version = langgraph.__version__
        except AttributeError:
            version = "Installed (version unavailable)"
        checks.append(("Package: langgraph", True, version))
    except ImportError:
        checks.append(("Package: langgraph", False, "Not installed"))
    
    try:
        import langchain
        checks.append(("Package: langchain", True, langchain.__version__))
    except ImportError:
        checks.append(("Package: langchain", False, "Not installed"))
    
    try:
        import openai
        checks.append(("Package: openai", True, openai.__version__))
    except ImportError:
        checks.append(("Package: openai", False, "Not installed"))
    
    try:
        import gspread
        checks.append(("Package: gspread", True, gspread.__version__))
    except ImportError:
        checks.append(("Package: gspread", False, "Not installed"))
    
    # Check API key
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    checks.append(("OpenAI API Key", bool(api_key), "Set" if api_key else "Missing"))
    
    # Check Google credentials
    creds_exist = Path('credentials.json').exists()
    checks.append(("Google Credentials", creds_exist, "Present" if creds_exist else "Missing"))
    
    # Print results
    print("\n" + "="*60)
    print("ENVIRONMENT CHECK RESULTS")
    print("="*60)
    
    all_passed = True
    for name, passed, details in checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} | {name}: {details}")
        if not passed:
            all_passed = False
    
    print("="*60)
    if all_passed:
        print("✅ All checks passed! Ready for testing.")
    else:
        print("❌ Some checks failed. Please fix before testing.")
    print("="*60 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = check_environment()
    sys.exit(0 if success else 1)
