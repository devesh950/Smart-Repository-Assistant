"""
Smart Repository Assistant - Issue Bot
Intelligent issue classification and auto-labeling system
"""

import re
from datetime import datetime
from github import Github
from textblob import TextBlob
from config import Config

class IssueClassifier:
    def __init__(self):
        self.config = Config()
        
    def classify_issue_type(self, title, body):
        """Classify issue type based on title and body content"""
        text = f"{title} {body}".lower()
        
        scores = {}
        for label, keywords in self.config.ISSUE_LABELS.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                scores[label] = score
        
        # Return the label with highest score, or 'general' if no matches
        return max(scores, key=scores.get) if scores else 'general'
    
    def determine_priority(self, title, body):
        """Determine priority based on content analysis"""
        text = f"{title} {body}".lower()
        
        for priority, keywords in self.config.PRIORITY_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return priority
        
        return 'medium'  # default priority
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of the issue text"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity < -0.3:
            return 'negative'
        elif polarity > 0.3:
            return 'positive'
        else:
            return 'neutral'
    
    def extract_components(self, body):
        """Extract mentioned components/modules from issue body"""
        components = []
        
        # Look for common patterns like file paths, modules, etc.
        patterns = [
            r'`([^`]+\.py)`',  # Python files in backticks
            r'`([^`]+\.js)`',  # JavaScript files
            r'`([^`]+\.html)`',  # HTML files
            r'in (\w+) module',  # Module mentions
            r'(\w+) component',  # Component mentions
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, body, re.IGNORECASE)
            components.extend(matches)
        
        return list(set(components))  # Remove duplicates

class SmartIssueBot:
    def __init__(self, github_token=None):
        self.github_token = github_token or Config.GITHUB_TOKEN
        self.github = Github(self.github_token)
        self.classifier = IssueClassifier()
        
    def process_issue(self, webhook_data):
        """Process incoming webhook data for issues"""
        try:
            action = webhook_data.get('action')
            issue_data = webhook_data.get('issue', {})
            
            if action not in ['opened', 'edited']:
                return
            
            repo_name = webhook_data['repository']['full_name']
            issue_number = issue_data['number']
            title = issue_data['title']
            body = issue_data['body'] or ''
            
            # Get repository and issue objects
            repo = self.github.get_repo(repo_name)
            issue = repo.get_issue(issue_number)
            
            # Classify and process the issue
            self._classify_and_label_issue(issue, title, body)
            
        except Exception as e:
            print(f"Error processing issue: {e}")
    
    def process_pull_request(self, webhook_data):
        """Process incoming webhook data for pull requests"""
        try:
            action = webhook_data.get('action')
            pr_data = webhook_data.get('pull_request', {})
            
            if action not in ['opened', 'edited']:
                return
            
            repo_name = webhook_data['repository']['full_name']
            pr_number = pr_data['number']
            title = pr_data['title']
            body = pr_data['body'] or ''
            
            # Get repository and PR objects
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            
            # Classify and process the PR
            self._classify_and_label_pr(pr, title, body)
            
        except Exception as e:
            print(f"Error processing PR: {e}")
    
    def _classify_and_label_issue(self, issue, title, body):
        """Classify issue and apply appropriate labels"""
        # Classify issue type
        issue_type = self.classifier.classify_issue_type(title, body)
        
        # Determine priority
        priority = self.classifier.determine_priority(title, body)
        
        # Analyze sentiment
        sentiment = self.classifier.analyze_sentiment(f"{title} {body}")
        
        # Extract components
        components = self.classifier.extract_components(body)
        
        # Apply labels
        labels_to_add = [issue_type]
        
        if priority != 'medium':
            labels_to_add.append(f"priority:{priority}")
        
        if sentiment == 'negative':
            labels_to_add.append('needs-attention')
        
        # Add component labels
        for component in components[:3]:  # Limit to 3 components
            labels_to_add.append(f"component:{component}")
        
        # Apply labels to the issue
        try:
            for label in labels_to_add:
                self._create_label_if_not_exists(issue.repository, label)
            
            issue.set_labels(*labels_to_add)
            
            # Add a comment explaining the auto-labeling
            comment = self._generate_auto_label_comment(issue_type, priority, components)
            issue.create_comment(comment)
            
        except Exception as e:
            print(f"Error applying labels: {e}")
    
    def _classify_and_label_pr(self, pr, title, body):
        """Classify PR and apply appropriate labels"""
        # Similar logic for PRs
        pr_type = self._classify_pr_type(title, body)
        
        labels_to_add = [pr_type]
        
        # Check PR size
        size_label = self._determine_pr_size(pr)
        if size_label:
            labels_to_add.append(size_label)
        
        # Apply labels
        try:
            for label in labels_to_add:
                self._create_label_if_not_exists(pr.base.repo, label)
            
            pr.set_labels(*labels_to_add)
            
        except Exception as e:
            print(f"Error applying PR labels: {e}")
    
    def _classify_pr_type(self, title, body):
        """Classify PR type based on title and content"""
        text = f"{title} {body}".lower()
        
        if any(word in text for word in ['fix', 'bug', 'error', 'issue']):
            return 'bugfix'
        elif any(word in text for word in ['feat', 'feature', 'add', 'new']):
            return 'feature'
        elif any(word in text for word in ['doc', 'documentation', 'readme']):
            return 'documentation'
        elif any(word in text for word in ['refactor', 'cleanup', 'improve']):
            return 'refactor'
        elif any(word in text for word in ['test', 'testing']):
            return 'test'
        else:
            return 'enhancement'
    
    def _determine_pr_size(self, pr):
        """Determine PR size based on changes"""
        additions = pr.additions
        deletions = pr.deletions
        total_changes = additions + deletions
        
        if total_changes < 20:
            return 'size:small'
        elif total_changes < 100:
            return 'size:medium'
        elif total_changes < 500:
            return 'size:large'
        else:
            return 'size:xl'
    
    def _create_label_if_not_exists(self, repo, label_name):
        """Create a label if it doesn't exist"""
        try:
            repo.get_label(label_name)
        except:
            # Label doesn't exist, create it
            color_map = {
                'bug': 'd73a4a',
                'feature': '0075ca',
                'documentation': '0052cc',
                'question': 'd876e3',
                'enhancement': 'a2eeef',
                'priority:critical': 'b60205',
                'priority:high': 'd93f0b',
                'priority:medium': 'fbca04',
                'priority:low': '0e8a16',
                'needs-attention': 'ff6b6b',
                'size:small': 'c2e0c6',
                'size:medium': 'f9d71c',
                'size:large': 'dfa878',
                'size:xl': 'd73a4a'
            }
            
            color = color_map.get(label_name.split(':')[0], '7057ff')
            if ':' in label_name:
                color = color_map.get(label_name, '7057ff')
            
            try:
                repo.create_label(label_name, color)
            except:
                pass  # Label might have been created concurrently
    
    def _generate_auto_label_comment(self, issue_type, priority, components):
        """Generate a helpful comment explaining the auto-labeling"""
        comment = f"🤖 **Auto-labeling complete!**\n\n"
        comment += f"- **Type**: {issue_type}\n"
        comment += f"- **Priority**: {priority}\n"
        
        if components:
            comment += f"- **Components**: {', '.join(components)}\n"
        
        comment += f"\n*This issue was automatically analyzed and labeled. "
        comment += f"If you think the labels are incorrect, please feel free to modify them.*"
        
        return comment

# Legacy function for backward compatibility
def process_issue(webhook_data):
    """Process issue webhook data (legacy function)"""
    bot = SmartIssueBot()
    
    if 'issue' in webhook_data:
        bot.process_issue(webhook_data)
    elif 'pull_request' in webhook_data:
        bot.process_pull_request(webhook_data)