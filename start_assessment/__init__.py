import azure.functions as func
import logging
import json
import uuid
import os
from datetime import datetime, timezone
from typing import Dict, Any

# Azure SDK imports
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos import PartitionKey
import openai

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Start Assessment API - Creates a new assessment session with a unique nickname
    
    POST /api/assessment
    Returns: 201 Created with sessionId and nickname
    """
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # Initialize Azure services
        cosmos_client_instance = get_cosmos_client()
        openai_client = get_openai_client()
        
        # Generate unique nickname
        nickname = generate_unique_nickname(cosmos_client_instance, openai_client)
        
        # Create session document
        session_id = str(uuid.uuid4())
        session_doc = create_session_document(session_id, nickname)
        
        # Save to Cosmos DB
        database_name = get_database_name()
        container_name = get_container_name()
        
        try:
            container = cosmos_client_instance.get_database_client(database_name).get_container_client(container_name)
            container.create_item(body=session_doc)
        except Exception as e:
            if "Owner resource does not exist" in str(e) or "NotFound" in str(e):
                logging.error(f"Database '{database_name}' or container '{container_name}' does not exist. Please create them first.")
                return func.HttpResponse(
                    json.dumps({"error": f"Database '{database_name}' or container '{container_name}' does not exist. Please create them first."}),
                    status_code=500,
                    mimetype="application/json"
                )
            else:
                raise e
        
        # Return success response
        response_data = {
            "sessionId": session_id,
            "nickname": nickname
        }
        
        return func.HttpResponse(
            json.dumps(response_data),
            status_code=201,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error in start_assessment: {str(e)}")
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

def get_openai_client():
    """Initialize and return Azure OpenAI client"""
    openai_endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
    openai_key = os.environ.get('AZURE_OPENAI_KEY')
    
    if not openai_endpoint or not openai_key:
        raise ValueError("Azure OpenAI credentials not configured")
    
    return openai.AzureOpenAI(
        azure_endpoint=openai_endpoint,
        api_key=openai_key,
        api_version="2024-02-15-preview"
    )

def generate_unique_nickname(cosmos_client_instance, openai_client, max_attempts=10):
    """Generate a unique nickname using Azure OpenAI and verify uniqueness in Cosmos DB"""
    
    database_name = get_database_name()
    container_name = get_container_name()
    container = cosmos_client_instance.get_database_client(database_name).get_container_client(container_name)
    
    for attempt in range(max_attempts):
        try:
            # Generate nickname using Azure OpenAI
            nickname = generate_nickname_with_openai(openai_client)
            
            # Check if nickname already exists
            if not nickname_exists_in_db(container, nickname):
                return nickname
                
        except Exception as e:
            logging.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_attempts - 1:
                raise Exception("Failed to generate unique nickname after maximum attempts")
    
    raise Exception("Failed to generate unique nickname")

def generate_nickname_with_openai(client):
    """Generate a nickname using Azure OpenAI GPT-3.5-turbo"""
    
    prompt = """Generate a unique, friendly nickname for a user taking an AI Navigator assessment. 
    The nickname should follow this format: [Color]-[Animal]-[Number]
    Examples: Crimson-Llama-42, Aqua-Badger-88, Emerald-Phoenix-15
    
    Requirements:
    - Use a color name (Crimson, Aqua, Emerald, etc.)
    - Use an animal name (Llama, Badger, Phoenix, etc.)
    - Use a random number between 10-99
    - Separate with hyphens
    - Keep it friendly and non-offensive
    
    Return only the nickname, nothing else."""
    
    response = client.chat.completions.create(
        model="gpt-35-turbo",  # Azure OpenAI model name
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates unique nicknames."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=20,
        temperature=0.8
    )
    
    nickname = response.choices[0].message.content.strip()
    
    # Validate nickname format
    if not is_valid_nickname_format(nickname):
        raise ValueError(f"Generated nickname '{nickname}' does not match expected format")
    
    return nickname

def is_valid_nickname_format(nickname):
    """Validate that nickname follows the expected format"""
    import re
    pattern = r'^[A-Z][a-z]+-[A-Z][a-z]+-\d{2}$'
    return bool(re.match(pattern, nickname))

def nickname_exists_in_db(container, nickname):
    """Check if nickname already exists in Cosmos DB"""
    try:
        # Query for existing nickname
        query = "SELECT VALUE COUNT(1) FROM c WHERE c.nickname = @nickname"
        parameters = [{"name": "@nickname", "value": nickname}]
        
        items = list(container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        return items[0] > 0
        
    except Exception as e:
        logging.error(f"Error checking nickname existence: {str(e)}")
        # If we can't check due to database/container not existing, assume unique
        if "Owner resource does not exist" in str(e) or "NotFound" in str(e):
            logging.info("Database or container doesn't exist yet, assuming nickname is unique")
            return False
        # For other errors, assume it exists to be safe
        return True

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