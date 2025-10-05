"""
GitHub App Configuration for Smart Repository Assistant
Enhanced configuration supporting both Personal Access Tokens and GitHub Apps
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # GitHub App Configuration (Recommended for production)
    GITHUB_APP_ID = os.getenv('GITHUB_APP_ID')
    GITHUB_APP_PRIVATE_KEY_PATH = os.getenv('GITHUB_APP_PRIVATE_KEY_PATH', 'private-key.pem')
    GITHUB_APP_INSTALLATION_ID = os.getenv('GITHUB_APP_INSTALLATION_ID')
    
    # Personal Access Token (For development/testing)
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
    # Webhook Configuration
    GITHUB_WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET')
    
    # Repository Configuration
    DEFAULT_REPO = os.getenv('DEFAULT_REPO', 'owner/repo-name')
    
    # Flask Configuration
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Analytics Configuration
    ANALYTICS_UPDATE_INTERVAL = int(os.getenv('ANALYTICS_UPDATE_INTERVAL', 3600))
    
    # Deployment Configuration
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')  # development, production
    
    # Issue Classification Labels
    ISSUE_LABELS = {
        'bug': ['bug', 'error', 'crash', 'broken', 'not working', 'fail'],
        'feature': ['feature', 'enhancement', 'new', 'add', 'implement'],
        'documentation': ['doc', 'documentation', 'readme', 'guide', 'help'],
        'question': ['question', 'help', 'how to', 'support'],
        'performance': ['performance', 'slow', 'optimization', 'speed'],
        'security': ['security', 'vulnerability', 'auth', 'permission'],
        'maintenance': ['maintenance', 'cleanup', 'refactor', 'update'],
        'ci/cd': ['ci', 'cd', 'build', 'deploy', 'pipeline', 'test']
    }
    
    # Priority Labels
    PRIORITY_KEYWORDS = {
        'critical': ['critical', 'urgent', 'emergency', 'blocking'],
        'high': ['high', 'important', 'asap'],
        'medium': ['medium', 'normal'],
        'low': ['low', 'minor', 'nice to have']
    }
    
    # Repository Health Thresholds
    HEALTH_THRESHOLDS = {
        'excellent': 90,
        'good': 75,
        'fair': 60,
        'poor': 40
    }
    
    @classmethod
    def is_github_app_configured(cls):
        """Check if GitHub App configuration is available"""
        return bool(cls.GITHUB_APP_ID and 
                   os.path.exists(cls.GITHUB_APP_PRIVATE_KEY_PATH) and 
                   cls.GITHUB_APP_INSTALLATION_ID)
    
    @classmethod
    def get_auth_method(cls):
        """Determine which authentication method to use"""
        if cls.is_github_app_configured():
            return 'github_app'
        elif cls.GITHUB_TOKEN:
            return 'personal_token'
        else:
            return None