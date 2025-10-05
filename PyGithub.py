"""
Smart Repository Assistant - GitHub Utilities
Helper functions and utilities for GitHub API operations
"""

from github import Github, GithubException
from config import Config
import time
import logging

logger = logging.getLogger(__name__)

class GitHubUtils:
    def __init__(self, token=None):
        self.token = token or Config.GITHUB_TOKEN
        self.github = Github(self.token)
        
    def get_rate_limit_info(self):
        """Get current rate limit information"""
        rate_limit = self.github.get_rate_limit()
        return {
            'core': {
                'limit': rate_limit.core.limit,
                'remaining': rate_limit.core.remaining,
                'reset': rate_limit.core.reset
            },
            'search': {
                'limit': rate_limit.search.limit,
                'remaining': rate_limit.search.remaining,
                'reset': rate_limit.search.reset
            }
        }
    
    def wait_for_rate_limit(self):
        """Wait if rate limit is exceeded"""
        rate_limit = self.github.get_rate_limit()
        if rate_limit.core.remaining < 10:
            reset_time = rate_limit.core.reset.timestamp()
            sleep_time = max(reset_time - time.time(), 0) + 1
            logger.info(f"Rate limit low, sleeping for {sleep_time:.1f} seconds")
            time.sleep(sleep_time)
    
    def get_repository_safely(self, repo_name):
        """Get repository with error handling"""
        try:
            self.wait_for_rate_limit()
            return self.github.get_repo(repo_name)
        except GithubException as e:
            logger.error(f"Error accessing repository {repo_name}: {e}")
            return None
    
    def create_issue_template(self, repo_name, template_type="bug_report"):
        """Create issue templates for the repository"""
        templates = {
            "bug_report": {
                "filename": "bug_report.md",
                "content": """---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Windows]
 - Browser [e.g. chrome, safari]
 - Version [e.g. 22]

**Additional context**
Add any other context about the problem here.
"""
            },
            "feature_request": {
                "filename": "feature_request.md",
                "content": """---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
"""
            }
        }
        
        try:
            repo = self.get_repository_safely(repo_name)
            if not repo:
                return False
            
            template = templates.get(template_type)
            if not template:
                return False
            
            # Create .github/ISSUE_TEMPLATE directory structure
            path = f".github/ISSUE_TEMPLATE/{template['filename']}"
            
            try:
                # Check if file exists
                repo.get_contents(path)
                logger.info(f"Template {path} already exists")
                return True
            except GithubException:
                # File doesn't exist, create it
                repo.create_file(
                    path=path,
                    message=f"Add {template_type} issue template",
                    content=template['content']
                )
                logger.info(f"Created issue template: {path}")
                return True
        
        except Exception as e:
            logger.error(f"Error creating issue template: {e}")
            return False
    
    def setup_repository_labels(self, repo_name):
        """Set up standard labels for the repository"""
        standard_labels = [
            {'name': 'bug', 'color': 'd73a4a', 'description': 'Something isn\'t working'},
            {'name': 'enhancement', 'color': 'a2eeef', 'description': 'New feature or request'},
            {'name': 'documentation', 'color': '0075ca', 'description': 'Improvements or additions to documentation'},
            {'name': 'question', 'color': 'd876e3', 'description': 'Further information is requested'},
            {'name': 'good first issue', 'color': '7057ff', 'description': 'Good for newcomers'},
            {'name': 'help wanted', 'color': '008672', 'description': 'Extra attention is needed'},
            {'name': 'priority:high', 'color': 'd93f0b', 'description': 'High priority'},
            {'name': 'priority:medium', 'color': 'fbca04', 'description': 'Medium priority'},
            {'name': 'priority:low', 'color': '0e8a16', 'description': 'Low priority'},
            {'name': 'size:small', 'color': 'c2e0c6', 'description': 'Small change'},
            {'name': 'size:medium', 'color': 'f9d71c', 'description': 'Medium change'},
            {'name': 'size:large', 'color': 'dfa878', 'description': 'Large change'},
        ]
        
        try:
            repo = self.get_repository_safely(repo_name)
            if not repo:
                return False
            
            existing_labels = {label.name for label in repo.get_labels()}
            
            for label_info in standard_labels:
                if label_info['name'] not in existing_labels:
                    try:
                        repo.create_label(
                            name=label_info['name'],
                            color=label_info['color'],
                            description=label_info.get('description', '')
                        )
                        logger.info(f"Created label: {label_info['name']}")
                    except GithubException as e:
                        logger.error(f"Error creating label {label_info['name']}: {e}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error setting up labels: {e}")
            return False
    
    def get_repository_languages(self, repo_name):
        """Get programming languages used in repository"""
        try:
            repo = self.get_repository_safely(repo_name)
            if not repo:
                return {}
            
            languages = repo.get_languages()
            total = sum(languages.values())
            
            # Calculate percentages
            language_stats = {}
            for lang, bytes_count in languages.items():
                percentage = (bytes_count / total * 100) if total > 0 else 0
                language_stats[lang] = {
                    'bytes': bytes_count,
                    'percentage': round(percentage, 2)
                }
            
            return language_stats
        
        except Exception as e:
            logger.error(f"Error getting repository languages: {e}")
            return {}
    
    def get_repository_topics(self, repo_name):
        """Get repository topics/tags"""
        try:
            repo = self.get_repository_safely(repo_name)
            if not repo:
                return []
            
            return repo.get_topics()
        
        except Exception as e:
            logger.error(f"Error getting repository topics: {e}")
            return []
    
    def add_repository_topics(self, repo_name, topics):
        """Add topics to repository"""
        try:
            repo = self.get_repository_safely(repo_name)
            if not repo:
                return False
            
            current_topics = set(repo.get_topics())
            new_topics = set(topics)
            all_topics = list(current_topics.union(new_topics))
            
            repo.replace_topics(all_topics)
            logger.info(f"Updated topics for {repo_name}: {all_topics}")
            return True
        
        except Exception as e:
            logger.error(f"Error adding topics: {e}")
            return False
    
    def create_pull_request_template(self, repo_name):
        """Create a pull request template"""
        template_content = """## Description
Brief description of the changes in this pull request.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] I have tested my changes
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings

## Screenshots (if applicable)
Add screenshots to help explain your changes.
"""
        
        try:
            repo = self.get_repository_safely(repo_name)
            if not repo:
                return False
            
            path = ".github/pull_request_template.md"
            
            try:
                repo.get_contents(path)
                logger.info("PR template already exists")
                return True
            except GithubException:
                repo.create_file(
                    path=path,
                    message="Add pull request template",
                    content=template_content
                )
                logger.info("Created PR template")
                return True
        
        except Exception as e:
            logger.error(f"Error creating PR template: {e}")
            return False

# Legacy compatibility functions
def create_issue_with_label(repo_name, title, body, label):
    """Create an issue with a specific label (legacy function)"""
    try:
        utils = GitHubUtils()
        repo = utils.get_repository_safely(repo_name)
        if not repo:
            return None
        
        issue = repo.create_issue(title=title, body=body, labels=[label])
        logger.info(f"Created issue #{issue.number}: {title}")
        return issue
    
    except Exception as e:
        logger.error(f"Error creating issue: {e}")
        return None

def add_label_to_issue(repo_name, issue_number, label):
    """Add label to existing issue (legacy function)"""
    try:
        utils = GitHubUtils()
        repo = utils.get_repository_safely(repo_name)
        if not repo:
            return False
        
        issue = repo.get_issue(issue_number)
        issue.add_to_labels(label)
        issue.create_comment(f"This issue has been auto-labeled as: {label}")
        
        logger.info(f"Added label '{label}' to issue #{issue_number}")
        return True
    
    except Exception as e:
        logger.error(f"Error adding label to issue: {e}")
        return False