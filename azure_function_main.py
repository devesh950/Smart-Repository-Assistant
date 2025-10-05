# Azure Functions configuration for Smart Repository Assistant
import azure.functions as func
import logging
import json
import os
from app import app as flask_app

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Functions entry point for webhook handling
    """
    logging.info('🚀 Smart Repository Assistant webhook triggered')
    
    try:
        # Get request data
        headers = dict(req.headers)
        body = req.get_body()
        method = req.method
        url = req.url
        
        # Create Flask test client
        with flask_app.test_client() as client:
            # Forward request to Flask app
            if method == 'POST':
                response = client.post(
                    '/webhook',
                    data=body,
                    headers=headers,
                    content_type='application/json'
                )
            elif method == 'GET':
                response = client.get('/health')
            else:
                return func.HttpResponse(
                    json.dumps({"error": "Method not allowed"}),
                    status_code=405,
                    headers={"Content-Type": "application/json"}
                )
            
            # Return response
            return func.HttpResponse(
                response.get_data(as_text=True),
                status_code=response.status_code,
                headers=dict(response.headers)
            )
            
    except Exception as e:
        logging.error(f"❌ Error processing webhook: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )