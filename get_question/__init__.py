import azure.functions as func
import logging
import json
import os
from typing import Dict, Any
from shared_session_storage import get_session

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Get Question API - Fetches the next question pair for a given session
    
    GET /api/assessment/{sessionId}/question
    OPTIONS /api/assessment/{sessionId}/question (for CORS preflight)
    Returns: 200 OK with question data or 404 if session not found
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
        # Get session ID from URL path
        session_id = req.route_params.get('sessionId')
        if not session_id:
            return func.HttpResponse(
                json.dumps({"error": "Session ID is required"}),
                status_code=400,
                mimetype="application/json",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization"
                }
            )
        
        # Get session from shared storage
        session = get_session(session_id)
        
        # Check if assessment is completed
        if session.get('status') == 'Completed':
            return func.HttpResponse(
                json.dumps({"error": "Assessment already completed"}),
                status_code=400,
                mimetype="application/json",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization"
                }
            )
        
        # Determine next question number based on existing answers
        current_answers = session.get('answers', [])
        next_question_number = len(current_answers) + 1
        
        # Check if all questions are completed
        if next_question_number > 40:
            return func.HttpResponse(
                json.dumps({"error": "All questions completed"}),
                status_code=400,
                mimetype="application/json",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization"
                }
            )
        
        # Get question pair data
        question_data = get_question_pair(next_question_number)
        
        # Return question data
        response_data = {
            "questionNumber": next_question_number,
            "totalQuestions": 40,
            "statements": question_data
        }
        
        return func.HttpResponse(
            json.dumps(response_data),
            status_code=200,
            mimetype="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            }
        )
        
    except Exception as e:
        logging.error(f"Error in get_question: {str(e)}")
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