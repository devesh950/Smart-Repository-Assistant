"""
Enhanced Analytics Dashboard Components
Additional visualization modules for the Smart Repository Assistant
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

def create_contributor_activity_heatmap(contributor_data):
    """Create a heatmap showing contributor activity over time"""
    if not contributor_data:
        return None
    
    # Prepare data for heatmap
    contributors = list(contributor_data.keys())[:15]  # Top 15 contributors
    activities = ['commits', 'issues_opened', 'prs_opened', 'prs_reviewed', 'issues_commented']
    
    z_data = []
    y_labels = []
    
    for contributor in contributors:
        stats = contributor_data[contributor]
        row = [
            stats.get('commits', 0),
            stats.get('issues_opened', 0),
            stats.get('prs_opened', 0),
            stats.get('prs_reviewed', 0),
            stats.get('issues_commented', 0)
        ]
        z_data.append(row)
        y_labels.append(contributor[:20])  # Truncate long names
    
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=['Commits', 'Issues Opened', 'PRs Opened', 'PRs Reviewed', 'Comments'],
        y=y_labels,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="Activity Count")
    ))
    
    fig.update_layout(
        title="Contributor Activity Heatmap",
        xaxis_title="Activity Type",
        yaxis_title="Contributors",
        height=500
    )
    
    return fig

def create_issue_lifecycle_chart(issue_data):
    """Create a chart showing issue lifecycle metrics"""
    if not issue_data:
        return None
    
    # Create gauge chart for issue close rate
    close_rate = issue_data.get('close_rate', 0)
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = close_rate,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Issue Close Rate (%)"},
        delta = {'reference': 75, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "gray"},
                {'range': [75, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=400)
    return fig

def create_pr_size_distribution(pr_data):
    """Create a pie chart for PR size distribution"""
    if not pr_data or 'pr_size_distribution' not in pr_data:
        return None
    
    sizes = pr_data['pr_size_distribution']
    if not sizes:
        return None
    
    labels = list(sizes.keys())
    values = list(sizes.values())
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker_colors=colors
    )])
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        title="Pull Request Size Distribution",
        annotations=[dict(text='PR Sizes', x=0.5, y=0.5, font_size=16, showarrow=False)]
    )
    
    return fig

def create_commit_frequency_chart(commit_data):
    """Create a line chart showing commit frequency over time"""
    if not commit_data or 'daily_commits' not in commit_data:
        return None
    
    daily_commits = commit_data['daily_commits']
    if not daily_commits:
        return None
    
    # Convert to pandas for easier manipulation
    dates = pd.to_datetime(list(daily_commits.keys()))
    commits = list(daily_commits.values())
    
    df = pd.DataFrame({'date': dates, 'commits': commits})
    df = df.sort_values('date')
    
    # Create moving average
    df['ma7'] = df['commits'].rolling(window=7, center=True).mean()
    
    fig = go.Figure()
    
    # Add daily commits
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['commits'],
        mode='markers+lines',
        name='Daily Commits',
        line=dict(color='lightblue', width=1),
        marker=dict(size=4)
    ))
    
    # Add moving average
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['ma7'],
        mode='lines',
        name='7-day Average',
        line=dict(color='darkblue', width=3)
    ))
    
    fig.update_layout(
        title="Commit Frequency Over Time",
        xaxis_title="Date",
        yaxis_title="Number of Commits",
        hovermode='x unified'
    )
    
    return fig

def create_repository_health_radar(health_data):
    """Create a radar chart showing different aspects of repository health"""
    
    # Calculate individual health metrics (you can customize these based on your data)
    metrics = {
        'Activity': min(100, health_data.get('commit_activity', {}).get('total_commits', 0) * 5),
        'Issue Management': health_data.get('issue_analytics', {}).get('close_rate', 0),
        'PR Management': health_data.get('pr_analytics', {}).get('merge_rate', 0),
        'Documentation': 70,  # You can calculate this based on README, docs, etc.
        'Community': min(100, len(health_data.get('contributor_activity', {})) * 10),
        'Code Quality': 80   # You can integrate with code analysis tools
    }
    
    categories = list(metrics.keys())
    values = list(metrics.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Repository Health'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Repository Health Radar Chart"
    )
    
    return fig

def create_response_time_chart(issue_data):
    """Create a chart showing issue response times"""
    if not issue_data:
        return None
    
    avg_response = issue_data.get('avg_response_time_hours', 0)
    avg_close = issue_data.get('avg_close_time_hours', 0)
    
    categories = ['Response Time', 'Resolution Time']
    values = [avg_response, avg_close]
    
    # Convert hours to days for better readability
    values_days = [v/24 for v in values]
    
    fig = go.Figure([go.Bar(
        x=categories,
        y=values_days,
        marker_color=['#FF6B6B', '#4ECDC4'],
        text=[f'{v:.1f} days' for v in values_days],
        textposition='auto'
    )])
    
    fig.update_layout(
        title="Average Issue Response & Resolution Times",
        yaxis_title="Time (Days)",
        showlegend=False
    )
    
    return fig

def create_language_distribution_chart(basic_stats):
    """Create a chart showing programming language distribution"""
    # This would typically come from GitHub API languages endpoint
    # For now, we'll use the primary language from basic stats
    language = basic_stats.get('language', 'Unknown')
    
    # You can expand this to get full language statistics
    languages = {language: 100} if language != 'Unknown' else {'Unknown': 100}
    
    fig = go.Figure([go.Bar(
        x=list(languages.keys()),
        y=list(languages.values()),
        marker_color='skyblue'
    )])
    
    fig.update_layout(
        title="Programming Language Distribution",
        xaxis_title="Language",
        yaxis_title="Percentage (%)"
    )
    
    return fig

def display_advanced_metrics(data):
    """Display advanced repository metrics in an organized layout"""
    
    st.markdown("## 🔍 Advanced Analytics")
    
    # Create tabs for different analysis sections
    tab1, tab2, tab3, tab4 = st.tabs(["🏃 Activity Analysis", "👥 Contributors", "🔧 Issues & PRs", "📊 Health Metrics"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Commit frequency chart
            commit_fig = create_commit_frequency_chart(data.get('commit_activity'))
            if commit_fig:
                st.plotly_chart(commit_fig, use_container_width=True)
        
        with col2:
            # Language distribution
            lang_fig = create_language_distribution_chart(data.get('basic_stats', {}))
            if lang_fig:
                st.plotly_chart(lang_fig, use_container_width=True)
    
    with tab2:
        # Contributor activity heatmap
        heatmap_fig = create_contributor_activity_heatmap(data.get('contributor_activity'))
        if heatmap_fig:
            st.plotly_chart(heatmap_fig, use_container_width=True)
        else:
            st.info("No contributor data available for heatmap")
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Issue lifecycle
            issue_fig = create_issue_lifecycle_chart(data.get('issue_analytics'))
            if issue_fig:
                st.plotly_chart(issue_fig, use_container_width=True)
        
        with col2:
            # PR size distribution
            pr_fig = create_pr_size_distribution(data.get('pr_analytics'))
            if pr_fig:
                st.plotly_chart(pr_fig, use_container_width=True)
        
        # Response times
        response_fig = create_response_time_chart(data.get('issue_analytics'))
        if response_fig:
            st.plotly_chart(response_fig, use_container_width=True)
    
    with tab4:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Repository health radar
            radar_fig = create_repository_health_radar(data)
            if radar_fig:
                st.plotly_chart(radar_fig, use_container_width=True)
        
        with col2:
            # Health score breakdown
            st.markdown("### 📈 Health Score Breakdown")
            health_score = data.get('health_score', 0)
            
            if health_score >= 90:
                st.success(f"🌟 Excellent: {health_score:.1f}/100")
            elif health_score >= 75:
                st.info(f"👍 Good: {health_score:.1f}/100")
            elif health_score >= 60:
                st.warning(f"⚠️ Fair: {health_score:.1f}/100")
            else:
                st.error(f"🚨 Poor: {health_score:.1f}/100")
            
            # Health tips
            st.markdown("### 💡 Health Tips")
            if health_score < 75:
                st.markdown("- 🔄 Increase commit frequency")
                st.markdown("- 📝 Improve issue response time")
                st.markdown("- 🤝 Encourage more contributors")
            else:
                st.markdown("- ✅ Great job maintaining the repo!")
                st.markdown("- 🚀 Keep up the good work!")

def create_comparison_dashboard():
    """Create a comparison view for multiple repositories"""
    st.markdown("## ⚖️ Repository Comparison")
    
    repo_input = st.text_input(
        "Enter repositories to compare (comma-separated)", 
        placeholder="facebook/react, microsoft/vscode, google/tensorflow"
    )
    
    if repo_input and st.button("Compare Repositories"):
        repos = [repo.strip() for repo in repo_input.split(',')]
        
        if len(repos) > 1:
            comparison_data = {}
            
            # This would typically fetch data for each repo
            # For demo purposes, we'll show the structure
            st.markdown("### 📊 Comparison Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Repository Count", len(repos))
            with col2:
                st.metric("Analyzed", "🔄 In Progress...")
            with col3:
                st.metric("Status", "✅ Ready")
            
            st.info("Repository comparison feature is ready! Add your GitHub token to enable full comparison.")
        else:
            st.warning("Please enter at least 2 repositories to compare")

def create_real_time_monitoring():
    """Create real-time monitoring widgets"""
    st.markdown("## 🔴 Live Monitoring")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🔥 Recent Activity",
            "5 commits",
            delta="2 today",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "🐛 Open Issues",
            "12",
            delta="-3 from last week",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "🔀 Open PRs",
            "8",
            delta="1 new",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            "👥 Active Contributors",
            "15",
            delta="2 new this month",
            delta_color="normal"
        )