"""
Smart Repository Assistant - Flask Application
Main webhook server and API endpoints
"""

import hmac
import hashlib
import json
from flask import Flask, request, jsonify, render_template_string
from werkzeug.exceptions import BadRequest
from issue_bot import SmartIssueBot, process_issue
from analytics import RepositoryAnalyzer
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.GITHUB_WEBHOOK_SECRET

# Initialize components
issue_bot = SmartIssueBot()

def verify_webhook_signature(payload_body, signature_header):
    """Verify GitHub webhook signature"""
    if not Config.GITHUB_WEBHOOK_SECRET:
        return True  # Skip verification if no secret configured
    
    if not signature_header:
        return False
    
    expected_signature = hmac.new(
        Config.GITHUB_WEBHOOK_SECRET.encode(),
        payload_body,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature_header)

@app.route("/", methods=["GET"])
def home():
    """Home page with basic information"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart Repository Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            .header { background: #f4f4f4; padding: 20px; border-radius: 5px; }
            .endpoint { background: #e8f4fd; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { color: #2196F3; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 Smart Repository Assistant</h1>
            <p>Intelligent GitHub repository management and analytics system</p>
        </div>
        
        <h2>Available Endpoints</h2>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/webhook</code><br>
            GitHub webhook endpoint for processing issues and pull requests
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/health</code><br>
            Get repository health score and status
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/analytics</code><br>
            Get comprehensive repository analytics
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/analytics/&lt;repo_name&gt;</code><br>
            Get analytics for a specific repository
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/analyze-issue</code><br>
            Manually analyze and label an issue
        </div>
        
        <h2>Dashboard</h2>
        <p>Access the analytics dashboard at: <a href="http://localhost:8501" target="_blank">http://localhost:8501</a></p>
        <p><em>Run: <code>streamlit run dashboard.py</code></em></p>
        
        <h2>Status</h2>
        <p>✅ Webhook server running</p>
        <p>✅ Issue bot active</p>
        <p>✅ Analytics engine ready</p>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route("/webhook", methods=["POST"])
def webhook():
    """GitHub webhook endpoint"""
    try:
        # Verify signature
        signature = request.headers.get('X-Hub-Signature-256')
        if not verify_webhook_signature(request.data, signature):
            logger.warning("Invalid webhook signature")
            return jsonify({"error": "Invalid signature"}), 401
        
        # Get event type
        event_type = request.headers.get('X-GitHub-Event')
        payload = request.get_json()
        
        if not payload:
            return jsonify({"error": "Invalid payload"}), 400
        
        logger.info(f"Received {event_type} event")
        
        # Process different event types
        if event_type == "issues":
            issue_bot.process_issue(payload)
            return jsonify({"message": "Issue processed successfully"}), 200
        
        elif event_type == "pull_request":
            issue_bot.process_pull_request(payload)
            return jsonify({"message": "Pull request processed successfully"}), 200
        
        elif event_type == "ping":
            return jsonify({"message": "Webhook is working!"}), 200
        
        else:
            logger.info(f"Unhandled event type: {event_type}")
            return jsonify({"message": f"Event {event_type} received but not processed"}), 200
    
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/health", methods=["GET"])
def health():
    """Get repository health information"""
    try:
        repo_name = request.args.get('repo', Config.DEFAULT_REPO)
        analyzer = RepositoryAnalyzer(repo_name)
        
        health_score = analyzer.calculate_health_score()
        basic_stats = analyzer.get_basic_stats()
        
        # Determine health status
        if health_score >= 90:
            status = "excellent"
        elif health_score >= 75:
            status = "good"
        elif health_score >= 60:
            status = "fair"
        else:
            status = "poor"
        
        return jsonify({
            "repository": repo_name,
            "health_score": health_score,
            "status": status,
            "basic_stats": basic_stats,
            "timestamp": analyzer.get_comprehensive_report()["generated_at"]
        })
    
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/analytics", methods=["GET"])
@app.route("/analytics/<path:repo_name>", methods=["GET"])
def analytics(repo_name=None):
    """Get comprehensive repository analytics"""
    try:
        if not repo_name:
            repo_name = request.args.get('repo', Config.DEFAULT_REPO)
        
        analyzer = RepositoryAnalyzer(repo_name)
        report = analyzer.get_comprehensive_report()
        
        # Add additional metadata
        report['api_version'] = '1.0'
        report['endpoints'] = {
            'webhook': '/webhook',
            'health': '/health',
            'analytics': '/analytics'
        }
        
        return jsonify(report)
    
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/analyze-issue", methods=["POST"])
def analyze_issue_manually():
    """Manually analyze and label an issue"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ['repo_name', 'issue_number']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        repo_name = data['repo_name']
        issue_number = data['issue_number']
        
        # Create mock webhook data
        mock_webhook = {
            'action': 'opened',
            'repository': {'full_name': repo_name},
            'issue': {'number': issue_number}
        }
        
        # Process the issue
        issue_bot.process_issue(mock_webhook)
        
        return jsonify({
            "message": "Issue analyzed successfully",
            "repo": repo_name,
            "issue": issue_number
        })
    
    except Exception as e:
        logger.error(f"Manual analysis error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/stats", methods=["GET"])
def quick_stats():
    """Get quick statistics for multiple repositories"""
    try:
        repos = request.args.get('repos', Config.DEFAULT_REPO).split(',')
        stats = {}
        
        for repo_name in repos[:5]:  # Limit to 5 repos
            repo_name = repo_name.strip()
            try:
                analyzer = RepositoryAnalyzer(repo_name)
                basic_stats = analyzer.get_basic_stats()
                health_score = analyzer.calculate_health_score()
                
                stats[repo_name] = {
                    'health_score': health_score,
                    'stars': basic_stats.get('stars', 0),
                    'forks': basic_stats.get('forks', 0),
                    'open_issues': basic_stats.get('open_issues', 0),
                    'language': basic_stats.get('language', 'Unknown')
                }
            except Exception as e:
                stats[repo_name] = {'error': str(e)}
        
        return jsonify(stats)
    
    except Exception as e:
        logger.error(f"Quick stats error: {e}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Custom 404 handler"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 handler"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logger.info("Starting Smart Repository Assistant...")
    logger.info(f"Webhook endpoint: http://{Config.FLASK_HOST}:{Config.FLASK_PORT}/webhook")
    logger.info(f"Health endpoint: http://{Config.FLASK_HOST}:{Config.FLASK_PORT}/health")
    logger.info(f"Analytics endpoint: http://{Config.FLASK_HOST}:{Config.FLASK_PORT}/analytics")
    
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )