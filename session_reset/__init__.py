import azure.functions as func
import logging
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any

# Azure SDK imports
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Session Reset API - Development/testing endpoint to reset a session
    
    POST /api/admin/sessions/{sessionId}/reset
    Returns: 200 OK with reset confirmation
    """
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # Get session ID from URL path
        session_id = req.route_params.get('sessionId')
        if not session_id:
            return func.HttpResponse(
                json.dumps({"error": "Session ID is required"}),
                status_code=400,
                mimetype="application/json"
            )

        # Initialize Cosmos DB client
        cosmos_client_instance = get_cosmos_client()

        # Get session from database
        session = get_session(cosmos_client_instance, session_id)
        if not session:
            return func.HttpResponse(
                json.dumps({"error": "Session not found"}),
                status_code=404,
                mimetype="application/json"
            )

        # Reset session to initial state
        reset_session(cosmos_client_instance, session_id, session)

        # Build response
        response_data = {
            "sessionId": session_id,
            "nickname": session.get('nickname'),
            "status": "InProgress",
            "resetAt": datetime.now(timezone.utc).isoformat(),
            "message": "Session reset successfully"
        }

        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error in session_reset: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )

def get_cosmos_client():
    """Initialize and return Cosmos DB client"""
    cosmos_endpoint = os.environ.get('COSMOS_ENDPOINT')
    cosmos_key = os.environ.get('COSMOS_KEY')
    
    if not cosmos_endpoint or not cosmos_key:
        raise ValueError("Cosmos DB credentials not configured")
    
    return cosmos_client.CosmosClient(cosmos_endpoint, cosmos_key)

def get_database_name():
    """Get database name from environment or use default"""
    return os.environ.get('COSMOS_DATABASE_NAME', 'navigator_profiler')

def get_container_name():
    """Get container name from environment or use default"""
    return os.environ.get('COSMOS_CONTAINER_NAME', 'sessions')

def get_session(cosmos_client_instance, session_id):
    """Retrieve session from Cosmos DB"""
    try:
        database_name = get_database_name()
        container_name = get_container_name()
        container = cosmos_client_instance.get_database_client(database_name).get_container_client(container_name)
        
        # Query for session by ID
        query = "SELECT * FROM c WHERE c.id = @session_id"
        parameters = [{"name": "@session_id", "value": session_id}]
        
        items = list(container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        return items[0] if items else None
        
    except Exception as e:
        logging.error(f"Error retrieving session: {str(e)}")
        return None

def reset_session(cosmos_client_instance, session_id, session):
    """Reset session to initial state"""
    try:
        database_name = get_database_name()
        container_name = get_container_name()
        container = cosmos_client_instance.get_database_client(database_name).get_container_client(container_name)
        
        # Reset session data
        session['status'] = 'InProgress'
        session['answers'] = []
        session['result'] = None
        session['completedAt'] = None
        session['reportFirstViewedAt'] = None
        
        # Update the session
        container.replace_item(item=session_id, body=session)
        
        logging.info(f"Session {session_id} reset successfully")
        
    except Exception as e:
        logging.error(f"Error resetting session: {str(e)}")
        raise e 