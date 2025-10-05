"""
Smart Repository Assistant - Analytics Module
Advanced repository analysis and health monitoring
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from github import Github
from config import Config
import json

class RepositoryAnalyzer:
    def __init__(self, repo_name=None, github_token=None):
        self.github_token = github_token or Config.GITHUB_TOKEN
        self.github = Github(self.github_token)
        self.repo_name = repo_name or Config.DEFAULT_REPO
        self.repo = self.github.get_repo(self.repo_name)
        self.cache = {}
        
    def get_basic_stats(self):
        """Get basic repository statistics"""
        try:
            stats = {
                'name': self.repo.name,
                'full_name': self.repo.full_name,
                'description': self.repo.description,
                'stars': self.repo.stargazers_count,
                'forks': self.repo.forks_count,
                'watchers': self.repo.watchers_count,
                'open_issues': self.repo.open_issues_count,
                'language': self.repo.language,
                'size': self.repo.size,
                'created_at': self.repo.created_at,
                'updated_at': self.repo.updated_at,
                'default_branch': self.repo.default_branch
            }
            return stats
        except Exception as e:
            print(f"Error getting basic stats: {e}")
            return {}
    
    def get_commit_activity(self, days=30):
        """Analyze commit activity over the last N days"""
        try:
            since = datetime.now() - timedelta(days=days)
            commits = list(self.repo.get_commits(since=since))
            
            # Daily commit counts
            daily_commits = defaultdict(int)
            commit_authors = defaultdict(int)
            commit_details = []
            
            for commit in commits:
                date = commit.commit.author.date.date()
                author = commit.commit.author.name
                
                daily_commits[date.isoformat()] += 1
                commit_authors[author] += 1
                
                commit_details.append({
                    'sha': commit.sha[:7],
                    'message': commit.commit.message.split('\n')[0][:100],
                    'author': author,
                    'date': commit.commit.author.date.isoformat(),
                    'additions': commit.stats.additions if commit.stats else 0,
                    'deletions': commit.stats.deletions if commit.stats else 0
                })
            
            return {
                'total_commits': len(commits),
                'daily_commits': dict(daily_commits),
                'top_contributors': dict(sorted(commit_authors.items(), 
                                              key=lambda x: x[1], reverse=True)[:10]),
                'commit_details': commit_details[:50]  # Latest 50 commits
            }
        except Exception as e:
            print(f"Error analyzing commit activity: {e}")
            return {}
    
    def get_issue_analytics(self):
        """Comprehensive issue analysis"""
        try:
            issues = list(self.repo.get_issues(state='all'))
            
            # Basic counts
            open_issues = [i for i in issues if i.state == 'open']
            closed_issues = [i for i in issues if i.state == 'closed']
            
            # Label analysis
            label_counts = Counter()
            priority_counts = Counter()
            
            # Time to close analysis
            close_times = []
            
            # Response times
            response_times = []
            
            for issue in issues:
                # Count labels
                for label in issue.labels:
                    label_counts[label.name] += 1
                    
                    if label.name.startswith('priority:'):
                        priority_counts[label.name] += 1
                
                # Calculate time to close
                if issue.state == 'closed' and issue.closed_at:
                    time_diff = (issue.closed_at - issue.created_at).total_seconds() / 3600  # hours
                    close_times.append(time_diff)
                
                # Calculate response time (time to first comment)
                comments = list(issue.get_comments())
                if comments:
                    first_comment = comments[0]
                    response_time = (first_comment.created_at - issue.created_at).total_seconds() / 3600
                    response_times.append(response_time)
            
            # Calculate averages
            avg_close_time = np.mean(close_times) if close_times else 0
            avg_response_time = np.mean(response_times) if response_times else 0
            
            return {
                'total_issues': len(issues),
                'open_issues': len(open_issues),
                'closed_issues': len(closed_issues),
                'close_rate': len(closed_issues) / len(issues) * 100 if issues else 0,
                'avg_close_time_hours': avg_close_time,
                'avg_response_time_hours': avg_response_time,
                'label_distribution': dict(label_counts.most_common(10)),
                'priority_distribution': dict(priority_counts),
                'issues_by_month': self._group_issues_by_month(issues)
            }
        except Exception as e:
            print(f"Error analyzing issues: {e}")
            return {}
    
    def get_pull_request_analytics(self):
        """Analyze pull request data"""
        try:
            pulls = list(self.repo.get_pulls(state='all'))
            
            open_prs = [p for p in pulls if p.state == 'open']
            closed_prs = [p for p in pulls if p.state == 'closed']
            merged_prs = [p for p in pulls if p.merged]
            
            # Size analysis
            pr_sizes = defaultdict(int)
            merge_times = []
            
            for pr in pulls:
                # Categorize by size
                total_changes = pr.additions + pr.deletions
                if total_changes < 20:
                    pr_sizes['small'] += 1
                elif total_changes < 100:
                    pr_sizes['medium'] += 1
                elif total_changes < 500:
                    pr_sizes['large'] += 1
                else:
                    pr_sizes['xl'] += 1
                
                # Calculate merge time
                if pr.merged_at:
                    merge_time = (pr.merged_at - pr.created_at).total_seconds() / 3600
                    merge_times.append(merge_time)
            
            return {
                'total_prs': len(pulls),
                'open_prs': len(open_prs),
                'merged_prs': len(merged_prs),
                'merge_rate': len(merged_prs) / len(pulls) * 100 if pulls else 0,
                'avg_merge_time_hours': np.mean(merge_times) if merge_times else 0,
                'pr_size_distribution': dict(pr_sizes)
            }
        except Exception as e:
            print(f"Error analyzing PRs: {e}")
            return {}
    
    def get_contributor_activity(self, days=90):
        """Analyze contributor activity and engagement"""
        try:
            since = datetime.now() - timedelta(days=days)
            
            # Get commits, issues, and PRs
            commits = list(self.repo.get_commits(since=since))
            issues = list(self.repo.get_issues(state='all', since=since))
            pulls = list(self.repo.get_pulls(state='all'))
            
            contributor_stats = defaultdict(lambda: {
                'commits': 0,
                'issues_opened': 0,
                'issues_commented': 0,
                'prs_opened': 0,
                'prs_reviewed': 0,
                'lines_added': 0,
                'lines_deleted': 0
            })
            
            # Analyze commits
            for commit in commits:
                author = commit.commit.author.name
                contributor_stats[author]['commits'] += 1
                if commit.stats:
                    contributor_stats[author]['lines_added'] += commit.stats.additions
                    contributor_stats[author]['lines_deleted'] += commit.stats.deletions
            
            # Analyze issues
            for issue in issues:
                author = issue.user.login if issue.user else 'Unknown'
                contributor_stats[author]['issues_opened'] += 1
                
                # Count comments
                for comment in issue.get_comments():
                    commenter = comment.user.login if comment.user else 'Unknown'
                    contributor_stats[commenter]['issues_commented'] += 1
            
            # Analyze PRs
            for pr in pulls:
                author = pr.user.login if pr.user else 'Unknown'
                contributor_stats[author]['prs_opened'] += 1
                
                # Count reviews
                for review in pr.get_reviews():
                    reviewer = review.user.login if review.user else 'Unknown'
                    contributor_stats[reviewer]['prs_reviewed'] += 1
            
            return dict(contributor_stats)
        except Exception as e:
            print(f"Error analyzing contributors: {e}")
            return {}
    
    def calculate_health_score(self):
        """Calculate overall repository health score (0-100)"""
        try:
            score = 0
            max_score = 100
            
            # Basic repo metrics (30 points)
            basic_stats = self.get_basic_stats()
            if basic_stats.get('description'):
                score += 5
            if basic_stats.get('stars', 0) > 10:
                score += 5
            if basic_stats.get('forks', 0) > 5:
                score += 5
            
            # Recent activity (25 points)
            commit_activity = self.get_commit_activity(30)
            recent_commits = commit_activity.get('total_commits', 0)
            if recent_commits > 0:
                score += min(15, recent_commits)  # Up to 15 points for commits
            
            # Issue management (25 points)
            issue_stats = self.get_issue_analytics()
            close_rate = issue_stats.get('close_rate', 0)
            score += min(15, close_rate * 0.15)  # Up to 15 points for close rate
            
            response_time = issue_stats.get('avg_response_time_hours', float('inf'))
            if response_time < 24:  # Less than 1 day
                score += 10
            elif response_time < 72:  # Less than 3 days
                score += 5
            
            # PR management (20 points)
            pr_stats = self.get_pull_request_analytics()
            merge_rate = pr_stats.get('merge_rate', 0)
            score += min(10, merge_rate * 0.1)  # Up to 10 points for merge rate
            
            merge_time = pr_stats.get('avg_merge_time_hours', float('inf'))
            if merge_time < 48:  # Less than 2 days
                score += 10
            elif merge_time < 168:  # Less than 1 week
                score += 5
            
            return min(100, max(0, score))
        except Exception as e:
            print(f"Error calculating health score: {e}")
            return 0
    
    def _group_issues_by_month(self, issues):
        """Group issues by month for trend analysis"""
        monthly_counts = defaultdict(lambda: {'opened': 0, 'closed': 0})
        
        for issue in issues:
            created_month = issue.created_at.strftime('%Y-%m')
            monthly_counts[created_month]['opened'] += 1
            
            if issue.closed_at:
                closed_month = issue.closed_at.strftime('%Y-%m')
                monthly_counts[closed_month]['closed'] += 1
        
        return dict(monthly_counts)
    
    def get_comprehensive_report(self):
        """Get a comprehensive analytics report"""
        try:
            return {
                'generated_at': datetime.now().isoformat(),
                'repository': self.repo_name,
                'basic_stats': self.get_basic_stats(),
                'health_score': self.calculate_health_score(),
                'commit_activity': self.get_commit_activity(),
                'issue_analytics': self.get_issue_analytics(),
                'pr_analytics': self.get_pull_request_analytics(),
                'contributor_activity': self.get_contributor_activity()
            }
        except Exception as e:
            print(f"Error generating comprehensive report: {e}")
            return {}
    
    def export_to_json(self, filename=None):
        """Export analytics data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"analytics_report_{timestamp}.json"
        
        report = self.get_comprehensive_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        return filename

# Legacy compatibility
def get_repo_analytics(repo_name):
    """Get repository analytics (legacy function)"""
    analyzer = RepositoryAnalyzer(repo_name)
    return analyzer.get_comprehensive_report()