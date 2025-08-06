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
    Submit Answer API - Handles user answer submissions for assessment questions
    
    POST /api/assessment/{sessionId}/answer
    Request Body: {"questionNumber": 1, "chosenStatementId": "A"}
    Returns: 204 No Content on success
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
            request_body = req.get_json()
        except Exception as e:
            return func.HttpResponse(
                json.dumps({"error": "Invalid JSON in request body"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Validate required fields
        question_number = request_body.get('questionNumber')
        chosen_statement_id = request_body.get('chosenStatementId')
        
        if question_number is None or chosen_statement_id is None:
            return func.HttpResponse(
                json.dumps({"error": "questionNumber and chosenStatementId are required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Validate question number range
        if not isinstance(question_number, int) or question_number < 1 or question_number > 40:
            return func.HttpResponse(
                json.dumps({"error": "questionNumber must be between 1 and 40"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Validate statement ID format
        if chosen_statement_id not in ['A', 'B']:
            return func.HttpResponse(
                json.dumps({"error": "chosenStatementId must be 'A' or 'B'"}),
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
        
        # Check if assessment is completed
        if session.get('status') == 'Completed':
            return func.HttpResponse(
                json.dumps({"error": "Assessment already completed"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Validate question progression
        current_answers = session.get('answers', [])
        expected_question_number = len(current_answers) + 1
        
        if question_number != expected_question_number:
            return func.HttpResponse(
                json.dumps({"error": f"Expected question {expected_question_number}, got {question_number}"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Check if this question was already answered
        for answer in current_answers:
            if answer.get('questionNumber') == question_number:
                return func.HttpResponse(
                    json.dumps({"error": f"Question {question_number} already answered"}),
                    status_code=400,
                    mimetype="application/json"
                )
        
        # Get question pair to validate the statement ID and get construct info
        question_pair = get_question_pair(question_number)
        if chosen_statement_id not in question_pair:
            return func.HttpResponse(
                json.dumps({"error": f"Invalid statement ID '{chosen_statement_id}' for question {question_number}"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Get the chosen statement details
        chosen_statement = question_pair[chosen_statement_id]
        chosen_construct = get_construct_for_statement_id(chosen_statement['id'])
        
        # Create answer record
        answer_record = {
            "questionNumber": question_number,
            "pairId": question_number,  # For MVP, pairId equals questionNumber
            "chosenStatementId": chosen_statement['id'],
            "chosenConstruct": chosen_construct
        }
        
        # Update session with new answer
        session['answers'].append(answer_record)
        
        # Check if this was the last question
        if len(session['answers']) == 40:
            session['status'] = 'Completed'
            session['completedAt'] = datetime.now(timezone.utc).isoformat()
        
        # Save updated session to database
        update_session(cosmos_client_instance, session)
        
        # Return success (204 No Content)
        return func.HttpResponse(
            status_code=204
        )
        
    except Exception as e:
        logging.error(f"Error in submit_answer: {str(e)}")
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

def update_session(cosmos_client_instance, session):
    """Update session in Cosmos DB"""
    try:
        database_name = get_database_name()
        container_name = get_container_name()
        container = cosmos_client_instance.get_database_client(database_name).get_container_client(container_name)
        
        # Replace the session document
        container.replace_item(item=session['id'], body=session)
        
    except Exception as e:
        logging.error(f"Error updating session: {str(e)}")
        raise e

def get_question_pair(question_number):
    """Get the question pair data for the given question number"""
    
    # Pre-generated question pairs from the Knowledge Base
    question_pairs = {
        1: {"A": {"id": 103, "text": "I like to analyze a problem from every angle before making a decision."}, 
             "B": {"id": 604, "text": "I find it easy to connect with people from different backgrounds."}},
        2: {"A": {"id": 204, "text": "I am willing to change my mind on an important issue when presented with a good argument."}, 
             "B": {"id": 1003, "text": "I believe that rules of fairness should apply to everyone equally, without exception."}},
        3: {"A": {"id": 303, "text": "I love learning new things just for the sake of learning."}, 
             "B": {"id": 902, "text": "I double-check my reasoning before committing to a final answer."}},
        4: {"A": {"id": 401, "text": "I am comfortable moving forward on a project even if all the details aren't finalized."}, 
             "B": {"id": 804, "text": "I'd rather build a quick prototype than spend a long time on a theoretical design."}},
        5: {"A": {"id": 505, "text": "I can listen to criticism about my ideas without getting defensive."}, 
             "B": {"id": 1002, "text": "Doing the right thing is more important to me than being popular."}},
        6: {"A": {"id": 602, "text": "I'm good at staying calm under pressure."}, 
             "B": {"id": 203, "text": "I think it is important to expose myself to opinions I strongly disagree with."}},
        7: {"A": {"id": 704, "text": "To solve a problem, I first try to understand its context and relationships."}, 
             "B": {"id": 305, "text": "I have a wide range of interests and am curious about many things."}},
        8: {"A": {"id": 1104, "text": "I assume that my coworkers are competent and reliable."}, 
             "B": {"id": 805, "text": "I like to experiment with different approaches to find the best one."}},
        9: {"A": {"id": 901, "text": "I tend to pause and think things through rather than relying on my gut instinct."}, 
             "B": {"id": 601, "text": "I am good at sensing what others are feeling, even if they don't say it."}},
        10: {"A": {"id": 504, "text": "I am comfortable saying 'I don't know' in a professional setting."}, 
              "B": {"id": 1001, "text": "I feel it's important to stick to principles of fairness, even if it makes things difficult."}},
        11: {"A": {"id": 104, "text": "I am drawn to tasks that require me to think deeply and concentrate."}, 
              "B": {"id": 302, "text": "The feeling of 'not knowing' something motivates me to find an answer."}},
        12: {"A": {"id": 201, "text": "I enjoy listening to arguments that challenge my current point of view."}, 
              "B": {"id": 504, "text": "I am comfortable saying 'I don't know' in a professional setting."}},
        13: {"A": {"id": 404, "text": "I can function well in situations where the rules are not clearly defined."}, 
              "B": {"id": 102, "text": "I get more satisfaction from a challenging mental task than an easy one."}},
        14: {"A": {"id": 802, "text": "I learn best by trying things out for myself."}, 
              "B": {"id": 1105, "text": "I prefer to rely on the goodwill of others rather than being suspicious."}},
        15: {"A": {"id": 701, "text": "I like to understand the big picture before diving into the individual components."}, 
              "B": {"id": 903, "text": "I am more of a reflective person than an impulsive one."}},
        16: {"A": {"id": 605, "text": "I am sensitive to the emotional needs of my colleagues."}, 
              "B": {"id": 503, "text": "I am aware that my own knowledge is limited and incomplete."}},
        17: {"A": {"id": 301, "text": "When I find a topic interesting, I feel a strong desire to learn everything about it."}, 
              "B": {"id": 703, "text": "When planning, I think about the ripple effects of a decision."}},
        18: {"A": {"id": 1004, "text": "I hold my ethical standards regardless of what others are doing."}, 
              "B": {"id": 602, "text": "I'm good at staying calm under pressure."}},
        19: {"A": {"id": 202, "text": "I actively look for evidence that might contradict my existing beliefs."}, 
              "B": {"id": 505, "text": "I can listen to criticism about my ideas without getting defensive."}},
        20: {"A": {"id": 403, "text": "Unexpected changes to a plan don't typically fluster me."}, 
              "B": {"id": 705, "text": "I naturally look for how different pieces of a project connect with each other."}},
        21: {"A": {"id": 105, "text": "I would rather do something that requires a lot of thought than something that is simple."}, 
              "B": {"id": 405, "text": "I find it energizing to work on problems where the final outcome is not yet clear."}},
        22: {"A": {"id": 801, "text": "My first instinct with a new tool is to start playing with it to see how it works."}, 
              "B": {"id": 1102, "text": "I generally assume people are telling the truth."}},
        23: {"A": {"id": 905, "text": "I prefer to carefully consider all options before making a choice."}, 
              "B": {"id": 502, "text": "I'm quick to admit when a task is beyond my current expertise."}},
        24: {"A": {"id": 1005, "text": "An unfair outcome for others is something I work hard to prevent."}, 
              "B": {"id": 205, "text": "I consider critiques of my ideas as a valuable opportunity to improve them."}},
        25: {"A": {"id": 303, "text": "I love learning new things just for the sake of learning."}, 
              "B": {"id": 605, "text": "I am sensitive to the emotional needs of my colleagues."}},
        26: {"A": {"id": 702, "text": "I often think about how small changes can impact the entire system."}, 
              "B": {"id": 304, "text": "If I hear a new term or concept, I'll often look it up immediately."}},
        27: {"A": {"id": 103, "text": "I like to analyze a problem from every angle before making a decision."}, 
              "B": {"id": 904, "text": "My gut feelings are something I check with logic, not something I blindly follow."}},
        28: {"A": {"id": 501, "text": "I readily accept that my own beliefs could be wrong."}, 
              "B": {"id": 1004, "text": "I hold my ethical standards regardless of what others are doing."}},
        29: {"A": {"id": 201, "text": "I enjoy listening to arguments that challenge my current point of view."}, 
              "B": {"id": 504, "text": "I am comfortable saying 'I don't know' in a professional setting."}},
        30: {"A": {"id": 402, "text": "I prefer jobs where my day-to-day tasks are varied and unpredictable."}, 
              "B": {"id": 803, "text": "I enjoy taking things apart to understand how they work."}},
        31: {"A": {"id": 1103, "text": "I find it easy to place my trust in others on a team."}, 
              "B": {"id": 102, "text": "I get more satisfaction from a challenging mental task than an easy one."}},
        32: {"A": {"id": 603, "text": "I'm often the person others come to for emotional support or advice."}, 
              "B": {"id": 903, "text": "I am more of a reflective person than an impulsive one."}},
        33: {"A": {"id": 703, "text": "When planning, I think about the ripple effects of a decision."}, 
              "B": {"id": 604, "text": "I find it easy to connect with people from different backgrounds."}},
        34: {"A": {"id": 305, "text": "I have a wide range of interests and am curious about many things."}, 
              "B": {"id": 901, "text": "I tend to pause and think things through rather than relying on my gut instinct."}},
        35: {"A": {"id": 105, "text": "I would rather do something that requires a lot of thought than something that is simple."}, 
              "B": {"id": 1105, "text": "I prefer to rely on the goodwill of others rather than being suspicious."}},
        36: {"A": {"id": 205, "text": "I consider critiques of my ideas as a valuable opportunity to improve them."}, 
              "B": {"id": 905, "text": "I prefer to carefully consider all options before making a choice."}},
        37: {"A": {"id": 805, "text": "I like to experiment with different approaches to find the best one."}, 
              "B": {"id": 1104, "text": "I assume that my coworkers are competent and reliable."}},
        38: {"A": {"id": 405, "text": "I find it energizing to work on problems where the final outcome is not yet clear."}, 
              "B": {"id": 802, "text": "I learn best by trying things out for myself."}},
        39: {"A": {"id": 1001, "text": "I feel it's important to stick to principles of fairness, even if it makes things difficult."}, 
              "B": {"id": 201, "text": "I enjoy listening to arguments that challenge my current point of view."}},
        40: {"A": {"id": 503, "text": "I am aware that my own knowledge is limited and incomplete."}, 
              "B": {"id": 303, "text": "I love learning new things just for the sake of learning."}}
    }
    
    if question_number not in question_pairs:
        raise ValueError(f"Question number {question_number} not found")
    
    return question_pairs[question_number]

def get_construct_for_statement_id(statement_id):
    """Get the construct name for a given statement ID"""
    
    # Mapping from statement ID to construct name
    construct_mapping = {
        # Need for Cognition
        101: "Need for Cognition", 102: "Need for Cognition", 103: "Need for Cognition", 
        104: "Need for Cognition", 105: "Need for Cognition",
        
        # Actively Open-Minded Thinking
        201: "Actively Open-Minded Thinking", 202: "Actively Open-Minded Thinking", 
        203: "Actively Open-Minded Thinking", 204: "Actively Open-Minded Thinking", 
        205: "Actively Open-Minded Thinking",
        
        # Epistemic Curiosity
        301: "Epistemic Curiosity", 302: "Epistemic Curiosity", 303: "Epistemic Curiosity", 
        304: "Epistemic Curiosity", 305: "Epistemic Curiosity",
        
        # Tolerance for Ambiguity
        401: "Tolerance for Ambiguity", 402: "Tolerance for Ambiguity", 
        403: "Tolerance for Ambiguity", 404: "Tolerance for Ambiguity", 
        405: "Tolerance for Ambiguity",
        
        # Intellectual Humility
        501: "Intellectual Humility", 502: "Intellectual Humility", 503: "Intellectual Humility", 
        504: "Intellectual Humility", 505: "Intellectual Humility",
        
        # Trait Emotional Intelligence
        601: "Trait Emotional Intelligence", 602: "Trait Emotional Intelligence", 
        603: "Trait Emotional Intelligence", 604: "Trait Emotional Intelligence", 
        605: "Trait Emotional Intelligence",
        
        # Holistic Thinking Preference
        701: "Holistic Thinking Preference", 702: "Holistic Thinking Preference", 
        703: "Holistic Thinking Preference", 704: "Holistic Thinking Preference", 
        705: "Holistic Thinking Preference",
        
        # Experimental Drive
        801: "Experimental Drive", 802: "Experimental Drive", 803: "Experimental Drive", 
        804: "Experimental Drive", 805: "Experimental Drive",
        
        # Deliberative Stance
        901: "Deliberative Stance", 902: "Deliberative Stance", 903: "Deliberative Stance", 
        904: "Deliberative Stance", 905: "Deliberative Stance",
        
        # Principled Ethics Orientation
        1001: "Principled Ethics Orientation", 1002: "Principled Ethics Orientation", 
        1003: "Principled Ethics Orientation", 1004: "Principled Ethics Orientation", 
        1005: "Principled Ethics Orientation",
        
        # General Trust Propensity
        1101: "General Trust Propensity", 1102: "General Trust Propensity", 
        1103: "General Trust Propensity", 1104: "General Trust Propensity", 
        1105: "General Trust Propensity"
    }
    
    return construct_mapping.get(statement_id, "Unknown") 