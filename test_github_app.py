"""
GitHub App Configuration Test
Test script to verify GitHub App setup and authentication
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from github_auth import get_github_client, get_auth_info
from config_github_app import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_github_app_setup():
    """Test GitHub App configuration and authentication"""
    
    print("🚀 GitHub App Setup Test")
    print("=" * 50)
    
    # Check authentication method
    auth_info = get_auth_info()
    print(f"📊 Authentication Method: {auth_info['method']}")
    print(f"🔧 GitHub App Configured: {auth_info['app_configured']}")
    print(f"🔑 Personal Token Configured: {auth_info['token_configured']}")
    print(f"🔗 Webhook Configured: {auth_info['webhook_configured']}")
    print()
    
    if auth_info['method'] is None:
        print("❌ No authentication method configured!")
        print("📋 Please set up either:")
        print("   1. GitHub App credentials (GITHUB_APP_ID, private key, GITHUB_APP_INSTALLATION_ID)")
        print("   2. Personal Access Token (GITHUB_TOKEN)")
        return False
    
    # Test GitHub client
    print("🔐 Testing GitHub Authentication...")
    try:
        github = get_github_client()
        
        # Test rate limit (this should work with any auth method)
        rate_limit = github.get_rate_limit()
        print(f"✅ Authentication successful!")
        print(f"📈 Rate Limit: {rate_limit.core.remaining}/{rate_limit.core.limit}")
        print(f"⏰ Reset Time: {rate_limit.core.reset}")
        print()
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False
    
    # Test repository access
    print("📂 Testing Repository Access...")
    try:
        repo_name = Config.DEFAULT_REPO
        repo = github.get_repo(repo_name)
        
        print(f"✅ Repository access successful!")
        print(f"📁 Repository: {repo.full_name}")
        print(f"⭐ Stars: {repo.stargazers_count}")
        print(f"🍴 Forks: {repo.forks_count}")
        print(f"💻 Language: {repo.language}")
        print()
        
    except Exception as e:
        print(f"❌ Repository access failed: {e}")
        print(f"💡 Make sure the repository '{repo_name}' exists and is accessible")
        return False
    
    # Test permissions
    print("🔒 Testing Permissions...")
    try:
        # Test if we can read issues
        issues = list(repo.get_issues(state='all'))[:5]
        print(f"✅ Can read issues: {len(issues)} issues found")
        
        # Test if we can read PRs
        prs = list(repo.get_pulls(state='all'))[:5]
        print(f"✅ Can read pull requests: {len(prs)} PRs found")
        
        # Check if we can potentially write (this doesn't actually write anything)
        permissions = repo.get_collaborator_permission(github.get_user())
        print(f"✅ Repository permissions: {permissions}")
        print()
        
    except Exception as e:
        print(f"⚠️ Limited permissions: {e}")
        print("💡 The app may have read-only access, which is fine for analytics")
        print()
    
    # Configuration summary
    print("📋 Configuration Summary:")
    print("-" * 30)
    if auth_info['method'] == 'github_app':
        print(f"🤖 Using GitHub App Authentication")
        print(f"   App ID: {Config.GITHUB_APP_ID}")
        print(f"   Private Key: {Config.GITHUB_APP_PRIVATE_KEY_PATH}")
        print(f"   Installation ID: {Config.GITHUB_APP_INSTALLATION_ID}")
    else:
        print(f"🔑 Using Personal Access Token")
        print(f"   Token: {'*' * 20}...{Config.GITHUB_TOKEN[-4:] if Config.GITHUB_TOKEN else 'Not set'}")
    
    print(f"🔗 Webhook Secret: {'Set' if Config.GITHUB_WEBHOOK_SECRET else 'Not set'}")
    print(f"📁 Default Repository: {Config.DEFAULT_REPO}")
    print(f"🌐 Flask Host: {Config.FLASK_HOST}:{Config.FLASK_PORT}")
    print()
    
    # Deployment recommendations
    print("🚀 Deployment Recommendations:")
    print("-" * 35)
    if auth_info['method'] == 'github_app':
        print("✅ GitHub App is configured - ready for production deployment!")
        print("📋 Next steps:")
        print("   1. Deploy to Heroku/Railway/Vercel")
        print("   2. Update webhook URL in GitHub App settings")
        print("   3. Test webhook integration")
    else:
        print("⚠️ Using Personal Access Token - consider upgrading to GitHub App for production")
        print("📋 Benefits of GitHub App:")
        print("   • Higher rate limits (5,000/hour)")
        print("   • Better security (scoped permissions)")
        print("   • Professional appearance")
    
    print()
    print("🎯 Webhook URL will be: https://your-app-domain.com/webhook")
    print("📊 Dashboard URL will be: https://your-app-domain.com")
    
    return True

def test_webhook_secret():
    """Test webhook secret configuration"""
    print("\n🔐 Webhook Configuration Test:")
    print("-" * 35)
    
    if Config.GITHUB_WEBHOOK_SECRET:
        print("✅ Webhook secret is configured")
        print(f"🔒 Secret length: {len(Config.GITHUB_WEBHOOK_SECRET)} characters")
        
        # Test webhook signature verification (mock)
        import hmac
        import hashlib
        
        test_payload = b'{"test": "payload"}'
        signature = hmac.new(
            Config.GITHUB_WEBHOOK_SECRET.encode(),
            test_payload,
            hashlib.sha256
        ).hexdigest()
        
        print(f"✅ Signature generation test passed")
        print(f"🔍 Sample signature: sha256={signature[:16]}...")
    else:
        print("⚠️ Webhook secret not configured")
        print("💡 Set GITHUB_WEBHOOK_SECRET for secure webhook integration")

if __name__ == "__main__":
    print()
    success = test_github_app_setup()
    test_webhook_secret()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 GitHub App setup test completed successfully!")
        print("🚀 Your Smart Repository Assistant is ready for deployment!")
    else:
        print("⚠️ Setup issues detected. Please review the configuration.")
    
    print("\n📖 For detailed setup instructions, see: GITHUB_APP_SETUP.md")
    print("🆘 Need help? Visit: https://github.com/devesh950/Smart-Repository-Assistant/issues")