"""
Smart Repository Assistant - Interactive Analytics Dashboard
Comprehensive visualization and monitoring interface
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from analytics import RepositoryAnalyzer
from config import Config

# Configure Streamlit page
st.set_page_config(
    page_title="Smart Repo Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border: 1px solid #e1e5e9;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .health-score-excellent { color: #28a745; }
    .health-score-good { color: #17a2b8; }
    .health-score-fair { color: #ffc107; }
    .health-score-poor { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_analytics_data(repo_name):
    """Load analytics data with caching"""
    try:
        analyzer = RepositoryAnalyzer(repo_name)
        return analyzer.get_comprehensive_report()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def display_health_score(score):
    """Display health score with color coding"""
    if score >= 90:
        color_class = "health-score-excellent"
        status = "Excellent"
    elif score >= 75:
        color_class = "health-score-good" 
        status = "Good"
    elif score >= 60:
        color_class = "health-score-fair"
        status = "Fair"
    else:
        color_class = "health-score-poor"
        status = "Poor"
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>Repository Health Score</h3>
        <h1 class="{color_class}">{score:.1f}/100</h1>
        <p>Status: <strong class="{color_class}">{status}</strong></p>
    </div>
    """, unsafe_allow_html=True)

def create_commit_activity_chart(commit_data):
    """Create commit activity visualization"""
    if not commit_data or 'daily_commits' not in commit_data:
        return None
    
    daily_commits = commit_data['daily_commits']
    if not daily_commits:
        return None
    
    dates = list(daily_commits.keys())
    counts = list(daily_commits.values())
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=counts,
        mode='lines+markers',
        name='Daily Commits',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Commit Activity (Last 30 Days)",
        xaxis_title="Date",
        yaxis_title="Number of Commits",
        hovermode='x unified'
    )
    
    return fig

def create_issue_analytics_charts(issue_data):
    """Create issue analytics visualizations"""
    charts = []
    
    if issue_data and 'label_distribution' in issue_data:
        # Label distribution pie chart
        labels = list(issue_data['label_distribution'].keys())
        values = list(issue_data['label_distribution'].values())
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3
        )])
        fig_pie.update_layout(title="Issue Label Distribution")
        charts.append(("Label Distribution", fig_pie))
    
    if issue_data and 'issues_by_month' in issue_data:
        # Monthly issue trends
        monthly_data = issue_data['issues_by_month']
        months = sorted(monthly_data.keys())
        opened = [monthly_data[month]['opened'] for month in months]
        closed = [monthly_data[month]['closed'] for month in months]
        
        fig_monthly = go.Figure()
        fig_monthly.add_trace(go.Bar(x=months, y=opened, name='Opened', marker_color='#ff6b6b'))
        fig_monthly.add_trace(go.Bar(x=months, y=closed, name='Closed', marker_color='#4ecdc4'))
        
        fig_monthly.update_layout(
            title="Monthly Issue Trends",
            xaxis_title="Month",
            yaxis_title="Number of Issues",
            barmode='group'
        )
        charts.append(("Monthly Trends", fig_monthly))
    
    return charts

def create_contributor_chart(contributor_data):
    """Create contributor activity visualization"""
    if not contributor_data:
        return None
    
    # Prepare data
    contributors = []
    commits = []
    issues = []
    prs = []
    
    for name, stats in list(contributor_data.items())[:10]:  # Top 10 contributors
        contributors.append(name)
        commits.append(stats['commits'])
        issues.append(stats['issues_opened'])
        prs.append(stats['prs_opened'])
    
    # Create subplot
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Commits', 'Issues Opened', 'PRs Opened'),
        specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "bar"}]]
    )
    
    fig.add_trace(go.Bar(x=contributors, y=commits, name="Commits"), row=1, col=1)
    fig.add_trace(go.Bar(x=contributors, y=issues, name="Issues"), row=1, col=2)
    fig.add_trace(go.Bar(x=contributors, y=prs, name="PRs"), row=1, col=3)
    
    fig.update_layout(
        title_text="Top Contributors Activity",
        showlegend=False,
        height=400
    )
    
    # Rotate x-axis labels
    fig.update_xaxes(tickangle=45)
    
    return fig

def display_key_metrics(data):
    """Display key metrics in columns"""
    basic_stats = data.get('basic_stats', {})
    issue_analytics = data.get('issue_analytics', {})
    pr_analytics = data.get('pr_analytics', {})
    commit_activity = data.get('commit_activity', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Issues",
            issue_analytics.get('total_issues', 0),
            delta=None
        )
        st.metric(
            "Open Issues", 
            issue_analytics.get('open_issues', 0)
        )
    
    with col2:
        st.metric(
            "Total PRs",
            pr_analytics.get('total_prs', 0)
        )
        st.metric(
            "Merge Rate",
            f"{pr_analytics.get('merge_rate', 0):.1f}%"
        )
    
    with col3:
        st.metric(
            "Recent Commits",
            commit_activity.get('total_commits', 0)
        )
        st.metric(
            "Contributors",
            len(commit_activity.get('top_contributors', {}))
        )
    
    with col4:
        st.metric(
            "Stars",
            basic_stats.get('stars', 0)
        )
        st.metric(
            "Forks",
            basic_stats.get('forks', 0)
        )

def main():
    """Main dashboard function"""
    st.title("🤖 Smart Repository Assistant")
    st.markdown("### Comprehensive GitHub Repository Analytics & Health Monitoring")
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    repo_name = st.sidebar.text_input(
        "Repository Name", 
        value=Config.DEFAULT_REPO,
        placeholder="owner/repo-name"
    )
    
    auto_refresh = st.sidebar.checkbox("Auto-refresh (every 5 minutes)", value=False)
    
    if st.sidebar.button("🔄 Refresh Data") or auto_refresh:
        st.cache_data.clear()
    
    # Export options
    st.sidebar.markdown("---")
    st.sidebar.header("Export Options")
    
    # Load data
    with st.spinner("Loading repository data..."):
        data = load_analytics_data(repo_name)
    
    if not data:
        st.error("Failed to load repository data. Please check your configuration.")
        return
    
    # Export functionality
    if st.sidebar.button("📊 Export JSON Report"):
        try:
            analyzer = RepositoryAnalyzer(repo_name)
            filename = analyzer.export_to_json()
            st.sidebar.success(f"Report exported to {filename}")
        except Exception as e:
            st.sidebar.error(f"Export failed: {e}")
    
    # Main content
    st.markdown("---")
    
    # Repository overview
    basic_stats = data.get('basic_stats', {})
    st.header(f"📊 {basic_stats.get('name', repo_name)}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Description:** {basic_stats.get('description', 'No description available')}")
        st.markdown(f"**Language:** {basic_stats.get('language', 'Not specified')}")
        st.markdown(f"**Created:** {basic_stats.get('created_at', 'Unknown')}")
        st.markdown(f"**Last Updated:** {basic_stats.get('updated_at', 'Unknown')}")
    
    with col2:
        # Health score
        health_score = data.get('health_score', 0)
        display_health_score(health_score)
    
    # Key metrics
    st.markdown("---")
    st.header("📈 Key Metrics")
    display_key_metrics(data)
    
    # Charts section
    st.markdown("---")
    st.header("📊 Analytics Charts")
    
    # Commit activity
    commit_fig = create_commit_activity_chart(data.get('commit_activity'))
    if commit_fig:
        st.plotly_chart(commit_fig, use_container_width=True)
    
    # Issue analytics
    col1, col2 = st.columns(2)
    
    issue_charts = create_issue_analytics_charts(data.get('issue_analytics'))
    for i, (title, chart) in enumerate(issue_charts):
        if i % 2 == 0:
            with col1:
                st.plotly_chart(chart, use_container_width=True)
        else:
            with col2:
                st.plotly_chart(chart, use_container_width=True)
    
    # Contributor activity
    contributor_fig = create_contributor_chart(data.get('contributor_activity'))
    if contributor_fig:
        st.plotly_chart(contributor_fig, use_container_width=True)
    
    # Advanced Analytics Section
    st.markdown("---")
    from dashboard_components import display_advanced_metrics, create_comparison_dashboard, create_real_time_monitoring
    
    # Display advanced metrics with beautiful visualizations
    display_advanced_metrics(data)
    
    # Real-time monitoring
    st.markdown("---")
    create_real_time_monitoring()
    
    # Repository comparison
    st.markdown("---")
    create_comparison_dashboard()
    
    # Detailed data tables
    st.markdown("---")
    st.header("📋 Detailed Data Tables")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Recent Commits", "🐛 Issue Analytics", "🔀 PR Analytics", "👥 Contributors"])
    
    with tab1:
        commit_activity = data.get('commit_activity', {})
        if 'commit_details' in commit_activity:
            df_commits = pd.DataFrame(commit_activity['commit_details'])
            st.dataframe(df_commits, use_container_width=True)
        else:
            st.info("No recent commit data available")
    
    with tab2:
        issue_analytics = data.get('issue_analytics', {})
        if issue_analytics:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Summary Metrics")
                st.json({
                    "Total Issues": issue_analytics.get('total_issues', 0),
                    "Open Issues": issue_analytics.get('open_issues', 0),
                    "Close Rate": f"{issue_analytics.get('close_rate', 0):.1f}%",
                    "Avg Response Time": f"{issue_analytics.get('avg_response_time_hours', 0):.1f} hours"
                })
            
            with col2:
                st.markdown("### 🏷️ Label Distribution")
                if 'label_distribution' in issue_analytics:
                    st.json(issue_analytics['label_distribution'])
        else:
            st.info("No issue analytics available")
    
    with tab3:
        pr_analytics = data.get('pr_analytics', {})
        if pr_analytics:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 PR Metrics")
                st.json({
                    "Total PRs": pr_analytics.get('total_prs', 0),
                    "Open PRs": pr_analytics.get('open_prs', 0),
                    "Merged PRs": pr_analytics.get('merged_prs', 0),
                    "Merge Rate": f"{pr_analytics.get('merge_rate', 0):.1f}%"
                })
            
            with col2:
                st.markdown("### 📏 Size Distribution")
                if 'pr_size_distribution' in pr_analytics:
                    st.json(pr_analytics['pr_size_distribution'])
        else:
            st.info("No PR analytics available")
    
    with tab4:
        contributor_activity = data.get('contributor_activity', {})
        if contributor_activity:
            # Create a more readable contributor table
            contributor_list = []
            for name, stats in contributor_activity.items():
                contributor_list.append({
                    'Contributor': name,
                    'Commits': stats.get('commits', 0),
                    'Issues': stats.get('issues_opened', 0),
                    'PRs': stats.get('prs_opened', 0),
                    'Reviews': stats.get('prs_reviewed', 0),
                    'Comments': stats.get('issues_commented', 0),
                    'Lines Added': stats.get('lines_added', 0),
                    'Lines Deleted': stats.get('lines_deleted', 0)
                })
            
            df_contributors = pd.DataFrame(contributor_list)
            df_contributors = df_contributors.sort_values('Commits', ascending=False)
            st.dataframe(df_contributors, use_container_width=True)
        else:
            st.info("No contributor data available")
    
    # Footer
    st.markdown("---")
    st.markdown("*Data generated at: " + data.get('generated_at', 'Unknown') + "*")
    
    # Auto-refresh logic
    if auto_refresh:
        st.experimental_rerun()

if __name__ == "__main__":
    main()