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
    Session Status API - Provides assessment progress information
    
    GET /api/assessment/{sessionId}/status
    Returns: 200 OK with session status and progress
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

        # Calculate progress
        answers = session.get('answers', [])
        total_questions = 40
        completed_questions = len(answers)
        progress_percentage = (completed_questions / total_questions) * 100

        # Determine status
        status = session.get('status', 'InProgress')
        
        # Get nickname
        nickname = session.get('nickname', 'Unknown')
        
        # Get timestamps
        created_at = session.get('createdAt')
        completed_at = session.get('completedAt')
        report_viewed_at = session.get('reportFirstViewedAt')

        # Format timestamps
        try:
            if created_at:
                created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                formatted_created = created_date.strftime("%B %d, %Y at %I:%M %p UTC")
            else:
                formatted_created = "Unknown"
        except:
            formatted_created = created_at or "Unknown"

        try:
            if completed_at:
                completed_date = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
                formatted_completed = completed_date.strftime("%B %d, %Y at %I:%M %p UTC")
            else:
                formatted_completed = None
        except:
            formatted_completed = completed_at

        # Build response
        response_data = {
            "sessionId": session_id,
            "nickname": nickname,
            "status": status,
            "progress": {
                "completedQuestions": completed_questions,
                "totalQuestions": total_questions,
                "percentage": round(progress_percentage, 1)
            },
            "timestamps": {
                "createdAt": formatted_created,
                "completedAt": formatted_completed,
                "reportViewedAt": report_viewed_at
            }
        }

        # Add result summary if completed
        if status == 'Completed' and session.get('result'):
            result = session.get('result', {})
            response_data["result"] = {
                "primaryArchetype": result.get('primaryArchetype'),
                "secondaryArchetype": result.get('secondaryArchetype'),
                "reportGenerated": bool(result.get('reportContent')),
                "reportViewed": bool(report_viewed_at)
            }

        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error in session_status: {str(e)}")
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