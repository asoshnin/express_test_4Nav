import azure.functions as func
import logging
import json
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

# Azure SDK imports
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Session Cleanup API - Admin endpoint to clean up old or abandoned sessions
    
    DELETE /api/admin/sessions/cleanup
    Query Parameters:
    - days (optional): Sessions older than this many days (default: 30)
    - status (optional): Only clean sessions with this status (InProgress, Completed)
    - dry_run (optional): If true, only return what would be deleted (default: false)
    Returns: 200 OK with cleanup results
    """
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # Get query parameters
        days = int(req.params.get('days', 30))
        status_filter = req.params.get('status')
        dry_run = req.params.get('dry_run', 'false').lower() == 'true'
        
        # Validate parameters
        if days < 1:
            return func.HttpResponse(
                json.dumps({"error": "Days must be at least 1"}),
                status_code=400,
                mimetype="application/json"
            )
        
        if status_filter and status_filter not in ['InProgress', 'Completed']:
            return func.HttpResponse(
                json.dumps({"error": "Status must be 'InProgress' or 'Completed'"}),
                status_code=400,
                mimetype="application/json"
            )

        # Initialize Cosmos DB client
        cosmos_client_instance = get_cosmos_client()

        # Calculate cutoff date
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        # Find sessions to clean up
        sessions_to_cleanup = find_sessions_to_cleanup(cosmos_client_instance, cutoff_date, status_filter)
        
        if dry_run:
            # Return what would be deleted
            response_data = {
                "dry_run": True,
                "sessions_found": len(sessions_to_cleanup),
                "cutoff_date": cutoff_date.isoformat(),
                "sessions": sessions_to_cleanup
            }
        else:
            # Actually delete the sessions
            deleted_count = delete_sessions(cosmos_client_instance, sessions_to_cleanup)
            
            response_data = {
                "dry_run": False,
                "sessions_deleted": deleted_count,
                "cutoff_date": cutoff_date.isoformat(),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error in session_cleanup: {str(e)}")
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

def find_sessions_to_cleanup(cosmos_client_instance, cutoff_date, status_filter=None):
    """Find sessions that should be cleaned up"""
    try:
        database_name = get_database_name()
        container_name = get_container_name()
        container = cosmos_client_instance.get_database_client(database_name).get_container_client(container_name)
        
        # Build query based on filters
        if status_filter:
            query = "SELECT * FROM c WHERE c.createdAt < @cutoff_date AND c.status = @status"
            parameters = [
                {"name": "@cutoff_date", "value": cutoff_date.isoformat()},
                {"name": "@status", "value": status_filter}
            ]
        else:
            query = "SELECT * FROM c WHERE c.createdAt < @cutoff_date"
            parameters = [{"name": "@cutoff_date", "value": cutoff_date.isoformat()}]
        
        items = list(container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        # Format sessions for response
        sessions = []
        for item in items:
            sessions.append({
                "id": item.get('id'),
                "nickname": item.get('nickname'),
                "status": item.get('status'),
                "createdAt": item.get('createdAt'),
                "completedAt": item.get('completedAt'),
                "answersCount": len(item.get('answers', []))
            })
        
        return sessions
        
    except Exception as e:
        logging.error(f"Error finding sessions to cleanup: {str(e)}")
        return []

def delete_sessions(cosmos_client_instance, sessions):
    """Delete sessions from Cosmos DB"""
    try:
        database_name = get_database_name()
        container_name = get_container_name()
        container = cosmos_client_instance.get_database_client(database_name).get_container_client(container_name)
        
        deleted_count = 0
        for session in sessions:
            try:
                container.delete_item(item=session['id'], partition_key=session['id'])
                deleted_count += 1
                logging.info(f"Deleted session {session['id']} ({session['nickname']})")
            except Exception as e:
                logging.error(f"Error deleting session {session['id']}: {str(e)}")
                continue
        
        return deleted_count
        
    except Exception as e:
        logging.error(f"Error deleting sessions: {str(e)}")
        return 0 