"""
Configuration settings for Smart Repository Assistant
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # GitHub Configuration
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    GITHUB_WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET')
    
    # Repository Configuration
    DEFAULT_REPO = os.getenv('DEFAULT_REPO', 'owner/repo-name')
    
    # Flask Configuration
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Analytics Configuration
    ANALYTICS_UPDATE_INTERVAL = int(os.getenv('ANALYTICS_UPDATE_INTERVAL', 3600))  # 1 hour
    
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