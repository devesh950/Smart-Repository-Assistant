"""
Smart Repository Assistant - Demo Script
Showcase the analytics dashboard features
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analytics import RepositoryAnalyzer
from config import Config
import json
from datetime import datetime

def demo_analytics_features():
    """Demonstrate all analytics features"""
    
    print("🚀 Smart Repository Assistant - Analytics Demo")
    print("=" * 60)
    
    # Initialize analyzer with your repository
    repo_name = Config.DEFAULT_REPO
    print(f"📊 Analyzing Repository: {repo_name}")
    print()
    
    try:
        analyzer = RepositoryAnalyzer(repo_name)
        
        # 1. Basic Repository Stats
        print("1️⃣ BASIC REPOSITORY INFORMATION")
        print("-" * 40)
        basic_stats = analyzer.get_basic_stats()
        
        print(f"   📂 Name: {basic_stats.get('name', 'Unknown')}")
        print(f"   📝 Description: {basic_stats.get('description', 'No description')}")
        print(f"   ⭐ Stars: {basic_stats.get('stars', 0)}")
        print(f"   🍴 Forks: {basic_stats.get('forks', 0)}")
        print(f"   👀 Watchers: {basic_stats.get('watchers', 0)}")
        print(f"   🐛 Open Issues: {basic_stats.get('open_issues', 0)}")
        print(f"   💻 Primary Language: {basic_stats.get('language', 'Unknown')}")
        print()
        
        # 2. Repository Health Score
        print("2️⃣ REPOSITORY HEALTH ANALYSIS")
        print("-" * 40)
        health_score = analyzer.calculate_health_score()
        
        if health_score >= 90:
            status_emoji = "🌟"
            status_text = "EXCELLENT"
        elif health_score >= 75:
            status_emoji = "👍"
            status_text = "GOOD"
        elif health_score >= 60:
            status_emoji = "⚠️"
            status_text = "FAIR"
        else:
            status_emoji = "🚨"
            status_text = "NEEDS IMPROVEMENT"
        
        print(f"   {status_emoji} Health Score: {health_score:.1f}/100 ({status_text})")
        print()
        
        # 3. Recent Activity
        print("3️⃣ RECENT COMMIT ACTIVITY (Last 30 Days)")
        print("-" * 40)
        commit_activity = analyzer.get_commit_activity(30)
        
        print(f"   📈 Total Commits: {commit_activity.get('total_commits', 0)}")
        print(f"   👥 Active Contributors: {len(commit_activity.get('top_contributors', {}))}")
        
        if commit_activity.get('top_contributors'):
            print("   🏆 Top Contributors:")
            for contributor, commits in list(commit_activity['top_contributors'].items())[:5]:
                print(f"      • {contributor}: {commits} commits")
        print()
        
        # 4. Issue Analytics
        print("4️⃣ ISSUE MANAGEMENT ANALYTICS")
        print("-" * 40)
        issue_analytics = analyzer.get_issue_analytics()
        
        print(f"   📊 Total Issues: {issue_analytics.get('total_issues', 0)}")
        print(f"   ✅ Closed Issues: {issue_analytics.get('closed_issues', 0)}")
        print(f"   🔄 Open Issues: {issue_analytics.get('open_issues', 0)}")
        print(f"   📈 Close Rate: {issue_analytics.get('close_rate', 0):.1f}%")
        
        if issue_analytics.get('avg_response_time_hours', 0) > 0:
            print(f"   ⏱️ Avg Response Time: {issue_analytics['avg_response_time_hours']:.1f} hours")
        
        if issue_analytics.get('label_distribution'):
            print("   🏷️ Most Used Labels:")
            for label, count in list(issue_analytics['label_distribution'].items())[:5]:
                print(f"      • {label}: {count} issues")
        print()
        
        # 5. Pull Request Analytics
        print("5️⃣ PULL REQUEST ANALYTICS")
        print("-" * 40)
        pr_analytics = analyzer.get_pull_request_analytics()
        
        print(f"   🔀 Total PRs: {pr_analytics.get('total_prs', 0)}")
        print(f"   ✅ Merged PRs: {pr_analytics.get('merged_prs', 0)}")
        print(f"   🔄 Open PRs: {pr_analytics.get('open_prs', 0)}")
        print(f"   📈 Merge Rate: {pr_analytics.get('merge_rate', 0):.1f}%")
        
        if pr_analytics.get('pr_size_distribution'):
            print("   📏 PR Size Distribution:")
            for size, count in pr_analytics['pr_size_distribution'].items():
                print(f"      • {size}: {count} PRs")
        print()
        
        # 6. Contributor Activity
        print("6️⃣ CONTRIBUTOR ENGAGEMENT (Last 90 Days)")
        print("-" * 40)
        contributor_activity = analyzer.get_contributor_activity(90)
        
        print(f"   👥 Active Contributors: {len(contributor_activity)}")
        
        if contributor_activity:
            print("   🌟 Top 5 Most Active Contributors:")
            # Sort by total activity (commits + issues + PRs)
            sorted_contributors = sorted(
                contributor_activity.items(),
                key=lambda x: x[1].get('commits', 0) + x[1].get('issues_opened', 0) + x[1].get('prs_opened', 0),
                reverse=True
            )
            
            for i, (contributor, stats) in enumerate(sorted_contributors[:5], 1):
                total_activity = stats.get('commits', 0) + stats.get('issues_opened', 0) + stats.get('prs_opened', 0)
                print(f"      {i}. {contributor}:")
                print(f"         • {stats.get('commits', 0)} commits")
                print(f"         • {stats.get('issues_opened', 0)} issues opened")
                print(f"         • {stats.get('prs_opened', 0)} PRs opened")
                print(f"         • Total Activity Score: {total_activity}")
        print()
        
        print("🎯 DASHBOARD FEATURES AVAILABLE:")
        print("-" * 40)
        print("   📊 Interactive Charts & Graphs")
        print("   🔥 Real-time Activity Heatmaps")
        print("   📈 Trend Analysis & Forecasting")
        print("   🎯 Health Score Monitoring")
        print("   👥 Contributor Activity Tracking")
        print("   🐛 Issue Lifecycle Analysis")
        print("   🔀 PR Size & Merge Analytics")
        print("   ⚖️ Multi-Repository Comparison")
        print("   🔴 Live Monitoring Dashboard")
        print()
        
        print("🌐 ACCESS YOUR ANALYTICS:")
        print("-" * 40)
        print("   📱 Dashboard: http://localhost:8501")
        print("   🔗 API Health: http://localhost:5000/health")
        print("   📊 API Analytics: http://localhost:5000/analytics")
        print("   🏠 Home Page: http://localhost:5000")
        print()
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("💡 Make sure your GitHub token is configured correctly in .env")
        return False
    
    return True

def show_available_charts():
    """Show what charts and graphs are available"""
    print("📊 AVAILABLE CHARTS & VISUALIZATIONS:")
    print("=" * 50)
    
    charts = [
        ("🔥 Activity Heatmap", "Shows contributor activity across different types"),
        ("📈 Commit Frequency", "Daily commit trends with moving averages"),
        ("🎯 Health Radar Chart", "Multi-dimensional repository health view"),
        ("🥧 Issue Label Pie Chart", "Distribution of issue types"),
        ("📊 PR Size Distribution", "Small, medium, large, XL pull requests"),
        ("⏱️ Response Time Chart", "Issue response and resolution times"),
        ("📉 Monthly Trends", "Issue open/close trends over time"),
        ("🎮 Health Score Gauge", "Real-time health monitoring gauge"),
        ("👥 Contributor Bar Charts", "Individual contributor statistics"),
        ("🌍 Language Distribution", "Programming languages used"),
        ("📋 Data Tables", "Detailed breakdowns and raw data"),
        ("⚖️ Repository Comparison", "Side-by-side repo analysis"),
        ("🔴 Live Monitoring", "Real-time metrics and alerts")
    ]
    
    for i, (chart_name, description) in enumerate(charts, 1):
        print(f"   {i:2d}. {chart_name}")
        print(f"       {description}")
    
    print()
    print("🎨 All charts are interactive with:")
    print("   • Hover tooltips")
    print("   • Zoom and pan capabilities")
    print("   • Export to PNG/HTML")
    print("   • Responsive design")
    print("   • Dark/light theme support")

if __name__ == "__main__":
    print()
    success = demo_analytics_features()
    print()
    show_available_charts()
    
    if success:
        print()
        print("🎉 SUCCESS! Your Smart Repository Assistant is fully operational!")
        print("🚀 Visit the dashboard to see all these analytics in action!")
    else:
        print()
        print("⚠️ Some features need configuration. Check your .env file!")