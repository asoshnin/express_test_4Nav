import azure.functions as func
import logging
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List

# Azure SDK imports
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Admin API - Retrieves all assessment sessions for administrative purposes
    
    GET /api/admin/assessments
    Query Parameters: 
    - status (optional): Filter by status (InProgress, Completed)
    - limit (optional): Limit number of results (default: 100)
    - offset (optional): Offset for pagination (default: 0)
    Returns: 200 OK with list of sessions
    """
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # Get query parameters
        status_filter = req.params.get('status')
        limit = int(req.params.get('limit', 100))
        offset = int(req.params.get('offset', 0))
        
        # Validate parameters
        if limit > 1000:
            return func.HttpResponse(
                json.dumps({"error": "Limit cannot exceed 1000"}),
                status_code=400,
                mimetype="application/json"
            )
        
        if offset < 0:
            return func.HttpResponse(
                json.dumps({"error": "Offset cannot be negative"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Initialize Cosmos DB client
        cosmos_client_instance = get_cosmos_client()
        
        # Get all sessions with optional filtering
        sessions = get_all_sessions(cosmos_client_instance, status_filter, limit, offset)
        
        # Calculate summary statistics
        summary = calculate_summary_statistics(cosmos_client_instance)
        
        # Prepare response
        response_data = {
            "sessions": sessions,
            "summary": summary,
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": len(sessions)
            }
        }
        
        return func.HttpResponse(
            json.dumps(response_data),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error in admin API: {str(e)}")
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

def get_all_sessions(cosmos_client_instance, status_filter=None, limit=100, offset=0):
    """Retrieve all sessions with optional filtering"""
    try:
        database_name = get_database_name()
        container_name = get_container_name()
        container = cosmos_client_instance.get_database_client(database_name).get_container_client(container_name)
        
        # Build query based on filters
        if status_filter:
            query = "SELECT * FROM c WHERE c.status = @status ORDER BY c.createdAt DESC OFFSET @offset LIMIT @limit"
            parameters = [
                {"name": "@status", "value": status_filter},
                {"name": "@offset", "value": offset},
                {"name": "@limit", "value": limit}
            ]
        else:
            query = "SELECT * FROM c ORDER BY c.createdAt DESC OFFSET @offset LIMIT @limit"
            parameters = [
                {"name": "@offset", "value": offset},
                {"name": "@limit", "value": limit}
            ]
        
        items = list(container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        # Sanitize sensitive data for admin view
        sanitized_items = []
        for item in items:
            sanitized_item = {
                "id": item.get('id'),
                "nickname": item.get('nickname'),
                "status": item.get('status'),
                "createdAt": item.get('createdAt'),
                "completedAt": item.get('completedAt'),
                "reportFirstViewedAt": item.get('reportFirstViewedAt'),
                "answersCount": len(item.get('answers', [])),
                "hasResult": 'result' in item,
                "primaryArchetype": item.get('result', {}).get('primaryArchetype'),
                "secondaryArchetype": item.get('result', {}).get('secondaryArchetype')
            }
            sanitized_items.append(sanitized_item)
        
        return sanitized_items
        
    except Exception as e:
        logging.error(f"Error retrieving sessions: {str(e)}")
        return []

def calculate_summary_statistics(cosmos_client_instance):
    """Calculate summary statistics for all sessions"""
    try:
        database_name = get_database_name()
        container_name = get_container_name()
        container = cosmos_client_instance.get_database_client(database_name).get_container_client(container_name)
        
        # Get total count
        total_query = "SELECT VALUE COUNT(1) FROM c"
        total_result = list(container.query_items(
            query=total_query,
            enable_cross_partition_query=True
        ))
        total_sessions = total_result[0] if total_result else 0
        
        # Get completed count
        completed_query = "SELECT VALUE COUNT(1) FROM c WHERE c.status = 'Completed'"
        completed_result = list(container.query_items(
            query=completed_query,
            enable_cross_partition_query=True
        ))
        completed_sessions = completed_result[0] if completed_result else 0
        
        # Get in progress count
        in_progress_query = "SELECT VALUE COUNT(1) FROM c WHERE c.status = 'InProgress'"
        in_progress_result = list(container.query_items(
            query=in_progress_query,
            enable_cross_partition_query=True
        ))
        in_progress_sessions = in_progress_result[0] if in_progress_result else 0
        
        # Get reports viewed count
        reports_viewed_query = "SELECT VALUE COUNT(1) FROM c WHERE IS_DEFINED(c.reportFirstViewedAt)"
        reports_viewed_result = list(container.query_items(
            query=reports_viewed_query,
            enable_cross_partition_query=True
        ))
        reports_viewed = reports_viewed_result[0] if reports_viewed_result else 0
        
        # Calculate completion rate
        completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
        
        return {
            "totalSessions": total_sessions,
            "completedSessions": completed_sessions,
            "inProgressSessions": in_progress_sessions,
            "reportsViewed": reports_viewed,
            "completionRate": round(completion_rate, 1)
        }
        
    except Exception as e:
        logging.error(f"Error calculating summary statistics: {str(e)}")
        return {
            "totalSessions": 0,
            "completedSessions": 0,
            "inProgressSessions": 0,
            "reportsViewed": 0,
            "completionRate": 0.0
        } 