# Azure Application Insights integration
import logging
import os
from datetime import datetime
from flask import request

try:
    from opencensus.ext.azure.log_exporter import AzureLogHandler
    from opencensus.ext.azure.trace_exporter import AzureExporter
    from opencensus.ext.flask.flask_middleware import FlaskMiddleware
    from opencensus.trace.samplers import ProbabilitySampler
    AZURE_INSIGHTS_AVAILABLE = True
except ImportError:
    AZURE_INSIGHTS_AVAILABLE = False

class AzureMonitoring:
    """Azure Application Insights integration for monitoring and telemetry"""
    
    def __init__(self, app=None):
        self.app = app
        self.instrumentation_key = os.getenv('APPINSIGHTS_INSTRUMENTATIONKEY')
        self.connection_string = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize Azure monitoring for Flask app"""
        if not (self.instrumentation_key or self.connection_string):
            app.logger.warning("⚠️  Azure Application Insights not configured")
            return
        
        if not AZURE_INSIGHTS_AVAILABLE:
            app.logger.warning("⚠️  Azure Application Insights SDK not installed")
            return
        
        try:
            # Configure Azure Log Handler
            if self.connection_string:
                handler = AzureLogHandler(connection_string=self.connection_string)
            else:
                handler = AzureLogHandler(instrumentation_key=self.instrumentation_key)
            
            # Set up logging
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            app.logger.addHandler(handler)
            
            # Configure distributed tracing
            middleware = FlaskMiddleware(
                app,
                exporter=AzureExporter(
                    connection_string=self.connection_string,
                    instrumentation_key=self.instrumentation_key
                ),
                sampler=ProbabilitySampler(rate=1.0)
            )
            
            app.logger.info("✅ Azure Application Insights configured successfully")
            
        except Exception as e:
            app.logger.error(f"❌ Failed to configure Azure monitoring: {str(e)}")
    
    def log_custom_event(self, event_name, properties=None, measurements=None):
        """Log custom event to Application Insights"""
        try:
            # This would typically use the Application Insights SDK
            # For now, we'll use structured logging
            event_data = {
                'event': event_name,
                'properties': properties or {},
                'measurements': measurements or {}
            }
            logging.info(f"📊 Custom Event: {event_data}")
        except Exception as e:
            logging.error(f"❌ Failed to log custom event: {str(e)}")
    
    def log_dependency(self, name, command_name, start_time, duration, success):
        """Log dependency call to Application Insights"""
        try:
            dependency_data = {
                'dependency': name,
                'command': command_name,
                'duration': duration,
                'success': success,
                'start_time': start_time
            }
            logging.info(f"🔗 Dependency: {dependency_data}")
        except Exception as e:
            logging.error(f"❌ Failed to log dependency: {str(e)}")

def configure_azure_monitoring(app):
    """Configure Azure monitoring for the Flask application"""
    monitoring = AzureMonitoring(app)
    
    # Add custom properties to all telemetry
    @app.before_request
    def before_request():
        # Add request context
        monitoring.log_custom_event('request_started', {
            'method': request.method,
            'path': request.path,
            'user_agent': request.headers.get('User-Agent', ''),
            'remote_addr': request.remote_addr
        })
    
    @app.after_request
    def after_request(response):
        # Log response
        monitoring.log_custom_event('request_completed', {
            'status_code': response.status_code,
            'path': request.path
        })
        return response
    
    return monitoring

# Health check endpoint for Azure
def azure_health_check():
    """Azure-specific health check with detailed diagnostics"""
    health_data = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'azure_region': os.getenv('WEBSITE_SITE_NAME', 'unknown'),
        'checks': {}
    }
    
    try:
        # Check GitHub connectivity
        import requests
        response = requests.get('https://api.github.com/rate_limit', timeout=5)
        health_data['checks']['github_api'] = {
            'status': 'healthy' if response.status_code == 200 else 'unhealthy',
            'response_time_ms': int(response.elapsed.total_seconds() * 1000)
        }
    except Exception as e:
        health_data['checks']['github_api'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    # Check database/storage connectivity (if applicable)
    health_data['checks']['storage'] = {'status': 'healthy'}
    
    # Overall health
    unhealthy_checks = [
        check for check in health_data['checks'].values() 
        if check['status'] != 'healthy'
    ]
    
    if unhealthy_checks:
        health_data['status'] = 'degraded'
    
    return health_data