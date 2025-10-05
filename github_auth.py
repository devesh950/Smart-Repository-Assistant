"""
GitHub App Authentication Module
Handles authentication for both GitHub Apps and Personal Access Tokens
"""

import jwt
import time
import requests
from github import Github, Auth
from config_github_app import Config
import logging

logger = logging.getLogger(__name__)

class GitHubAuthManager:
    def __init__(self):
        self.config = Config()
        self.auth_method = self.config.get_auth_method()
        self._github_client = None
        
    def get_github_client(self):
        """Get authenticated GitHub client"""
        if self._github_client is None:
            if self.auth_method == 'github_app':
                self._github_client = self._get_app_client()
            elif self.auth_method == 'personal_token':
                self._github_client = self._get_token_client()
            else:
                raise Exception("No GitHub authentication configured")
        
        return self._github_client
    
    def _get_app_client(self):
        """Get GitHub client using GitHub App authentication"""
        try:
            # Generate JWT for the GitHub App
            app_jwt = self._generate_app_jwt()
            
            # Get installation access token
            installation_token = self._get_installation_token(app_jwt)
            
            # Create authenticated GitHub client
            auth = Auth.Token(installation_token)
            return Github(auth=auth)
            
        except Exception as e:
            logger.error(f"Failed to authenticate with GitHub App: {e}")
            raise
    
    def _get_token_client(self):
        """Get GitHub client using Personal Access Token"""
        try:
            auth = Auth.Token(self.config.GITHUB_TOKEN)
            return Github(auth=auth)
        except Exception as e:
            logger.error(f"Failed to authenticate with Personal Token: {e}")
            raise
    
    def _generate_app_jwt(self):
        """Generate JWT for GitHub App authentication"""
        try:
            # Read private key
            with open(self.config.GITHUB_APP_PRIVATE_KEY_PATH, 'r') as key_file:
                private_key = key_file.read()
            
            # Create JWT payload
            now = int(time.time())
            payload = {
                'iat': now - 60,  # Issued 60 seconds ago
                'exp': now + (10 * 60),  # Expires in 10 minutes
                'iss': self.config.GITHUB_APP_ID  # GitHub App ID
            }
            
            # Generate JWT
            token = jwt.encode(payload, private_key, algorithm='RS256')
            return token
            
        except Exception as e:
            logger.error(f"Failed to generate JWT: {e}")
            raise
    
    def _get_installation_token(self, app_jwt):
        """Get installation access token using the App JWT"""
        try:
            headers = {
                'Authorization': f'Bearer {app_jwt}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            url = f'https://api.github.com/app/installations/{self.config.GITHUB_APP_INSTALLATION_ID}/access_tokens'
            
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            
            return response.json()['token']
            
        except Exception as e:
            logger.error(f"Failed to get installation token: {e}")
            raise
    
    def get_auth_info(self):
        """Get information about current authentication"""
        return {
            'method': self.auth_method,
            'app_configured': self.config.is_github_app_configured(),
            'token_configured': bool(self.config.GITHUB_TOKEN),
            'webhook_configured': bool(self.config.GITHUB_WEBHOOK_SECRET)
        }

# Global auth manager instance
auth_manager = GitHubAuthManager()

def get_github_client():
    """Convenience function to get authenticated GitHub client"""
    return auth_manager.get_github_client()

def get_auth_info():
    """Get authentication information"""
    return auth_manager.get_auth_info()