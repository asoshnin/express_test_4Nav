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
    Contact Submission API - Handles user contact form submissions
    
    POST /api/assessment/{sessionId}/contact
    Request Body: {"name": "John Doe", "email": "john@example.com", "message": "I'd like to learn more..."}
    Returns: 201 Created on success
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
        
        # Parse request body
        try:
            req_body = req.get_json()
            name = req_body.get('name')
            email = req_body.get('email')
            message = req_body.get('message')
        except ValueError:
            return func.HttpResponse(
                json.dumps({"error": "Invalid JSON body"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Validate required fields
        if not all([name, email, message]):
            return func.HttpResponse(
                json.dumps({"error": "name, email, and message are required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            return func.HttpResponse(
                json.dumps({"error": "Invalid email format"}),
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
        
        # Create contact submission record
        contact_submission = {
            "id": f"{session_id}_contact_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
            "sessionId": session_id,
            "nickname": session.get('nickname', 'Unknown'),
            "name": name,
            "email": email,
            "message": message,
            "submittedAt": datetime.now(timezone.utc).isoformat(),
            "status": "New"
        }
        
        # Store contact submission in Cosmos DB
        store_contact_submission(cosmos_client_instance, contact_submission)
        
        return func.HttpResponse(
            json.dumps({"message": "Contact submission received successfully"}),
            status_code=201,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error in contact submission: {str(e)}")
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

def store_contact_submission(cosmos_client_instance, contact_submission):
    """Store contact submission in Cosmos DB"""
    try:
        database_name = get_database_name()
        container_name = get_container_name()
        container = cosmos_client_instance.get_database_client(database_name).get_container_client(container_name)
        
        # Insert the contact submission
        container.create_item(body=contact_submission)
        
        logging.info(f"Contact submission stored for session {contact_submission['sessionId']}")
        
    except Exception as e:
        logging.error(f"Error storing contact submission: {str(e)}")
        raise 