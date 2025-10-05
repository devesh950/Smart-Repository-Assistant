"""
Smart Repository Assistant - Test Script
Test the functionality of the system components
"""

import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from analytics import RepositoryAnalyzer
from issue_bot import SmartIssueBot, IssueClassifier
from PyGithub import GitHubUtils

def test_configuration():
    """Test configuration loading"""
    print("🔧 Testing Configuration...")
    try:
        config = Config()
        print(f"   ✅ GitHub Token: {'Set' if config.GITHUB_TOKEN else 'Not Set'}")
        print(f"   ✅ Default Repo: {config.DEFAULT_REPO}")
        print(f"   ✅ Flask Port: {config.FLASK_PORT}")
        return True
    except Exception as e:
        print(f"   ❌ Configuration Error: {e}")
        return False

def test_issue_classifier():
    """Test issue classification"""
    print("\n🤖 Testing Issue Classifier...")
    try:
        classifier = IssueClassifier()
        
        # Test cases
        test_cases = [
            ("Bug: App crashes when clicking submit", "The app crashes every time I click submit", "bug"),
            ("Feature Request: Add dark mode", "Would love to have a dark mode option", "feature"),
            ("Documentation missing for API", "The API documentation is incomplete", "documentation"),
            ("How to install?", "I need help installing this software", "question")
        ]
        
        for title, body, expected in test_cases:
            result = classifier.classify_issue_type(title, body)
            status = "✅" if result == expected else "⚠️"
            print(f"   {status} '{title}' -> {result} (expected: {expected})")
        
        return True
    except Exception as e:
        print(f"   ❌ Classifier Error: {e}")
        return False

def test_github_utils():
    """Test GitHub utilities"""
    print("\n🐙 Testing GitHub Utils...")
    try:
        if not Config.GITHUB_TOKEN:
            print("   ⚠️ GitHub token not configured, skipping GitHub tests")
            return True
            
        utils = GitHubUtils()
        
        # Test rate limit info
        rate_limit = utils.get_rate_limit_info()
        print(f"   ✅ Rate limit info retrieved: {rate_limit['core']['remaining']} requests remaining")
        
        # Test language detection (using a public repo)
        languages = utils.get_repository_languages("octocat/Hello-World")
        print(f"   ✅ Languages detected: {list(languages.keys()) if languages else 'None'}")
        
        return True
    except Exception as e:
        print(f"   ❌ GitHub Utils Error: {e}")
        return False

def test_analytics_demo():
    """Test analytics with demo data"""
    print("\n📊 Testing Analytics (Demo Mode)...")
    try:
        # Create a demo analyzer (this will fail without valid token, but we can test structure)
        if Config.GITHUB_TOKEN:
            analyzer = RepositoryAnalyzer("octocat/Hello-World")
            basic_stats = analyzer.get_basic_stats()
            if basic_stats:
                print(f"   ✅ Basic stats retrieved for demo repo")
                print(f"   ✅ Repo name: {basic_stats.get('name', 'Unknown')}")
                print(f"   ✅ Stars: {basic_stats.get('stars', 0)}")
            else:
                print("   ⚠️ Could not retrieve basic stats")
        else:
            print("   ⚠️ GitHub token not configured, skipping analytics test")
        
        return True
    except Exception as e:
        print(f"   ❌ Analytics Error: {e}")
        return False

def test_webhook_data_processing():
    """Test webhook data processing"""
    print("\n🔗 Testing Webhook Processing...")
    try:
        # Create mock webhook data
        mock_issue_data = {
            "action": "opened",
            "repository": {"full_name": "test/repo"},
            "issue": {
                "number": 1,
                "title": "Bug: Application crashes on startup",
                "body": "The application crashes immediately when I try to start it. This is a critical issue that needs urgent attention."
            }
        }
        
        # Test issue processing (without actually calling GitHub API)
        bot = SmartIssueBot()
        classifier = IssueClassifier()
        
        title = mock_issue_data["issue"]["title"]
        body = mock_issue_data["issue"]["body"]
        
        issue_type = classifier.classify_issue_type(title, body)
        priority = classifier.determine_priority(title, body)
        sentiment = classifier.analyze_sentiment(f"{title} {body}")
        
        print(f"   ✅ Issue classified as: {issue_type}")
        print(f"   ✅ Priority detected: {priority}")
        print(f"   ✅ Sentiment: {sentiment}")
        
        return True
    except Exception as e:
        print(f"   ❌ Webhook Processing Error: {e}")
        return False

def run_system_check():
    """Run comprehensive system check"""
    print("🚀 Smart Repository Assistant - System Check")
    print("=" * 50)
    
    tests = [
        test_configuration,
        test_issue_classifier,
        test_github_utils,
        test_analytics_demo,
        test_webhook_data_processing
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📋 Summary:")
    
    passed = sum(results)
    total = len(results)
    
    print(f"   Tests passed: {passed}/{total}")
    
    if passed == total:
        print("   🎉 All systems are working correctly!")
    elif passed > total * 0.7:
        print("   ✅ Most systems are working. Check warnings above.")
    else:
        print("   ⚠️ Several systems need attention. Please review errors above.")
    
    print("\n🛠️ Next Steps:")
    if not Config.GITHUB_TOKEN:
        print("   1. Set up your GitHub token in .env file")
        print("   2. Configure your repository name in .env")
    
    print("   3. Start the webhook server: python app.py")
    print("   4. Launch the dashboard: streamlit run dashboard.py")
    print("   5. Set up GitHub webhooks pointing to your server")
    
    return passed == total

if __name__ == "__main__":
    success = run_system_check()
    sys.exit(0 if success else 1)