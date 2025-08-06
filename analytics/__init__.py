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
    Analytics API - Provides system metrics and usage statistics
    
    GET /api/admin/analytics
    Query Parameters:
    - period (optional): "24h", "7d", "30d", "all" (default: "7d")
    Returns: 200 OK with analytics data
    """
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # Get query parameters
        period = req.params.get('period', '7d')
        
        # Validate period parameter
        valid_periods = ['24h', '7d', '30d', 'all']
        if period not in valid_periods:
            return func.HttpResponse(
                json.dumps({"error": f"Invalid period. Must be one of: {', '.join(valid_periods)}"}),
                status_code=400,
                mimetype="application/json"
            )

        # Initialize Cosmos DB client
        cosmos_client_instance = get_cosmos_client()

        # Calculate date filter
        date_filter = calculate_date_filter(period)
        
        # Get analytics data
        analytics_data = get_analytics_data(cosmos_client_instance, date_filter)

        # Build response
        response_data = {
            "period": period,
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "metrics": analytics_data
        }

        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error in analytics: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )

def calculate_date_filter(period):
    """Calculate the date filter based on period"""
    now = datetime.now(timezone.utc)
    
    if period == '24h':
        return now - timedelta(days=1)
    elif period == '7d':
        return now - timedelta(days=7)
    elif period == '30d':
        return now - timedelta(days=30)
    else:  # 'all'
        return None

def get_analytics_data(cosmos_client_instance, date_filter):
    """Get analytics data from Cosmos DB"""
    try:
        database_name = get_database_name()
        container_name = get_container_name()
        container = cosmos_client_instance.get_database_client(database_name).get_container_client(container_name)

        # Build query based on date filter
        if date_filter:
            query = "SELECT * FROM c WHERE c.createdAt >= @date_filter"
            parameters = [{"name": "@date_filter", "value": date_filter.isoformat()}]
        else:
            query = "SELECT * FROM c"
            parameters = []

        # Execute query
        items = list(container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

        # Calculate metrics
        total_sessions = len(items)
        completed_sessions = len([item for item in items if item.get('status') == 'Completed'])
        in_progress_sessions = len([item for item in items if item.get('status') == 'InProgress'])
        
        # Calculate completion rate
        completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
        
        # Calculate average completion time
        completion_times = []
        for item in items:
            if item.get('status') == 'Completed' and item.get('createdAt') and item.get('completedAt'):
                try:
                    created = datetime.fromisoformat(item['createdAt'].replace('Z', '+00:00'))
                    completed = datetime.fromisoformat(item['completedAt'].replace('Z', '+00:00'))
                    duration = (completed - created).total_seconds() / 60  # minutes
                    completion_times.append(duration)
                except:
                    continue
        
        avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0
        
        # Calculate archetype distribution
        archetype_counts = {}
        for item in items:
            if item.get('status') == 'Completed' and item.get('result'):
                primary = item['result'].get('primaryArchetype')
                if primary:
                    archetype_counts[primary] = archetype_counts.get(primary, 0) + 1
        
        # Calculate report generation stats
        reports_generated = len([item for item in items if item.get('result', {}).get('reportContent')])
        reports_viewed = len([item for item in items if item.get('reportFirstViewedAt')])
        
        # Calculate daily activity (last 7 days)
        daily_activity = {}
        for i in range(7):
            date = (datetime.now(timezone.utc) - timedelta(days=i)).strftime('%Y-%m-%d')
            daily_activity[date] = 0
        
        for item in items:
            if item.get('createdAt'):
                try:
                    created = datetime.fromisoformat(item['createdAt'].replace('Z', '+00:00'))
                    date_key = created.strftime('%Y-%m-%d')
                    if date_key in daily_activity:
                        daily_activity[date_key] += 1
                except:
                    continue

        return {
            "sessions": {
                "total": total_sessions,
                "completed": completed_sessions,
                "inProgress": in_progress_sessions,
                "completionRate": round(completion_rate, 1)
            },
            "performance": {
                "averageCompletionTimeMinutes": round(avg_completion_time, 1),
                "reportsGenerated": reports_generated,
                "reportsViewed": reports_viewed,
                "reportViewRate": round((reports_viewed / reports_generated * 100) if reports_generated > 0 else 0, 1)
            },
            "archetypeDistribution": archetype_counts,
            "dailyActivity": daily_activity,
            "periodStats": {
                "startDate": date_filter.isoformat() if date_filter else "all time",
                "endDate": datetime.now(timezone.utc).isoformat()
            }
        }

    except Exception as e:
        logging.error(f"Error getting analytics data: {str(e)}")
        return {
            "sessions": {"total": 0, "completed": 0, "inProgress": 0, "completionRate": 0},
            "performance": {"averageCompletionTimeMinutes": 0, "reportsGenerated": 0, "reportsViewed": 0, "reportViewRate": 0},
            "archetypeDistribution": {},
            "dailyActivity": {},
            "periodStats": {"startDate": "all time", "endDate": datetime.now(timezone.utc).isoformat()}
        }

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