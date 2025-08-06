import azure.functions as func
import logging
import json
import os
from datetime import datetime, timezone

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Health Check API - Verifies service availability
    
    GET /api/health
    Returns: 200 OK with service status
    """
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # Check if required environment variables are set
        required_env_vars = [
            'COSMOS_ENDPOINT',
            'COSMOS_KEY',
            'AZURE_OPENAI_ENDPOINT',
            'AZURE_OPENAI_KEY'
        ]
        
        missing_vars = []
        for var in required_env_vars:
            if not os.environ.get(var):
                missing_vars.append(var)
        
        # Determine health status
        if missing_vars:
            status = "degraded"
            message = f"Missing environment variables: {', '.join(missing_vars)}"
        else:
            status = "healthy"
            message = "All systems operational"
        
        # Create response
        response_data = {
            "status": status,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
            "service": "AI Navigator Profiler API",
            "environment": os.environ.get('AZURE_FUNCTIONS_ENVIRONMENT', 'local')
        }
        
        # Return appropriate status code
        status_code = 200 if status == "healthy" else 503
        
        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            status_code=status_code,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error in health check: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "status": "error",
                "message": "Health check failed",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "error": str(e)
            }),
            status_code=500,
            mimetype="application/json"
        ) 