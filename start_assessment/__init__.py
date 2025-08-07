import azure.functions as func
import logging
import json
import uuid
import os
from datetime import datetime, timezone
from typing import Dict, Any
from shared_session_storage import update_session

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Start Assessment API - Creates a new assessment session with a unique nickname
    
    POST /api/assessment
    OPTIONS /api/assessment (for CORS preflight)
    Returns: 201 Created with sessionId and nickname
    """
    logging.info('Python HTTP trigger function processed a request.')
    
    # Handle CORS preflight requests
    if req.method == "OPTIONS":
        return func.HttpResponse(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
                "Access-Control-Max-Age": "86400"
            }
        )
    
    try:
        # Generate unique nickname (simplified for testing)
        nickname = generate_simple_nickname()
        
        # Create session document
        session_id = str(uuid.uuid4())
        session_doc = create_session_document(session_id, nickname)
        
        # Save session to shared storage for testing
        update_session(session_doc)
        
        # Return success response
        response_data = {
            "sessionId": session_id,
            "nickname": nickname
        }
        
        return func.HttpResponse(
            json.dumps(response_data),
            status_code=201,
            mimetype="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            }
        )
        
    except Exception as e:
        logging.error(f"Error in start_assessment: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            }
        )

def generate_simple_nickname():
    """Generate a simple nickname for testing"""
    import random
    
    colors = ["Crimson", "Aqua", "Emerald", "Azure", "Violet", "Amber", "Sage", "Coral"]
    animals = ["Llama", "Badger", "Phoenix", "Dragon", "Wolf", "Eagle", "Lion", "Tiger"]
    number = random.randint(10, 99)
    
    color = random.choice(colors)
    animal = random.choice(animals)
    
    return f"{color}-{animal}-{number}"

def create_session_document(session_id, nickname):
    """Create a new session document for Cosmos DB"""
    
    now = datetime.now(timezone.utc).isoformat()
    
    return {
        "id": session_id,
        "nickname": nickname,
        "contactEmail": None,
        "status": "InProgress",
        "createdAt": now,
        "completedAt": None,
        "reportFirstViewedAt": None,
        "answers": [],
        "result": None
    } 