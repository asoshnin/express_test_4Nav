import azure.functions as func
import logging
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List
from shared_session_storage import get_session, update_session

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Generate Report API - Creates personalized assessment report
    
    GET /api/assessment/{sessionId}/report
    OPTIONS /api/assessment/{sessionId}/report (for CORS preflight)
    Returns: 200 OK with report data or 410 if already viewed
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
        if not session:
            return func.HttpResponse(
                json.dumps({"error": "Session not found"}),
                status_code=404,
                mimetype="application/json",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization"
                }
            )
        
        # Check if assessment is completed
        if session.get('status') != 'Completed':
            return func.HttpResponse(
                json.dumps({"error": "Assessment not completed"}),
                status_code=400,
                mimetype="application/json",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization"
                }
            )
        
        # Check if report has already been viewed
        if session.get('reportFirstViewedAt'):
            return func.HttpResponse(
                json.dumps({"error": "Report already viewed"}),
                status_code=410,
                mimetype="application/json",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization"
                }
            )
        
        # Calculate scores and generate report
        result = calculate_scores_and_generate_report(session)
        
        # Update session with report data and mark as viewed
        session['result'] = result
        session['reportFirstViewedAt'] = datetime.now(timezone.utc).isoformat()
        update_session(session)
        
        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            }
        )
        
    except Exception as e:
        logging.error(f"Error in generate_report: {str(e)}")
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

def calculate_scores_and_generate_report(session):
    """Calculate scores from answers and generate personalized report"""
    
    # Get answers from session
    answers = session.get('answers', [])
    nickname = session.get('nickname', 'Unknown')
    
    # Calculate construct scores
    construct_scores = calculate_construct_scores(answers)
    
    # Calculate archetype scores
    archetype_scores = calculate_archetype_scores(construct_scores)
    
    # Determine primary and secondary archetypes
    sorted_archetypes = sorted(archetype_scores, key=lambda x: x['score'], reverse=True)
    primary_archetype = sorted_archetypes[0]
    secondary_archetype = sorted_archetypes[1] if len(sorted_archetypes) > 1 else None
    
    # Generate personalized report
    report_content = create_fallback_report(nickname, primary_archetype, secondary_archetype)
    
    # Create result object
    result = {
        "primaryArchetype": primary_archetype['name'],
        "secondaryArchetype": secondary_archetype['name'] if secondary_archetype else None,
        "scores": {
            "archetypes": archetype_scores,
            "constructs": construct_scores
        },
        "reportContent": report_content
    }
    
    return result

def calculate_construct_scores(answers):
    """Calculate scores for each of the 11 constructs"""
    
    # Initialize construct counters
    construct_counts = {
        "Need for Cognition": 0,
        "Actively Open-Minded Thinking": 0,
        "Epistemic Curiosity": 0,
        "Tolerance for Ambiguity": 0,
        "Intellectual Humility": 0,
        "Trait Emotional Intelligence": 0,
        "Holistic Thinking Preference": 0,
        "Experimental Drive": 0,
        "Deliberative Stance": 0,
        "Principled Ethics Orientation": 0,
        "General Trust Propensity": 0
    }
    
    # Map statement IDs to constructs
    statement_to_construct = get_statement_to_construct_mapping()
    
    # Count choices for each construct
    for answer in answers:
        chosen_statement_id = answer.get('chosenStatementId')
        if chosen_statement_id in statement_to_construct:
            construct = statement_to_construct[chosen_statement_id]
            construct_counts[construct] += 1
    
    # Convert to percentile scores (simplified for MVP)
    # In a real implementation, these would be based on norm group data
    construct_scores = []
    for construct, count in construct_counts.items():
        # Simple percentile calculation based on max possible score
        max_possible = 40  # Total questions
        percentile = min(95, max(5, (count / max_possible) * 100))
        
        construct_scores.append({
            "name": construct,
            "score": count,
            "percentile": round(percentile, 1)
        })
    
    return construct_scores

def calculate_archetype_scores(construct_scores):
    """Calculate archetype scores based on construct scores"""
    
    # Create lookup for construct scores
    construct_lookup = {score['name']: score['score'] for score in construct_scores}
    
    # Archetype formulas from the Knowledge Base
    archetypes = [
        {
            "name": "The Critical Interrogator",
            "formula": [
                "Need for Cognition",
                "Actively Open-Minded Thinking", 
                "Epistemic Curiosity",
                "Intellectual Humility",
                "Deliberative Stance"
            ]
        },
        {
            "name": "The Human-Centric Strategist",
            "formula": [
                "Trait Emotional Intelligence",
                "Holistic Thinking Preference",
                "Principled Ethics Orientation",
                "General Trust Propensity"
            ]
        },
        {
            "name": "The Curious Experimenter",
            "formula": [
                "Tolerance for Ambiguity",
                "Experimental Drive",
                "Epistemic Curiosity",
                "Actively Open-Minded Thinking"
            ]
        }
    ]
    
    archetype_scores = []
    for archetype in archetypes:
        score = sum(construct_lookup.get(construct, 0) for construct in archetype['formula'])
        # Calculate percentile (simplified for MVP)
        max_possible = 40  # Total questions
        percentile = min(95, max(5, (score / max_possible) * 100))
        
        archetype_scores.append({
            "name": archetype['name'],
            "score": score,
            "percentile": round(percentile, 1)
        })
    
    return archetype_scores

def get_statement_to_construct_mapping():
    """Map statement IDs to their corresponding constructs"""
    return {
        101: "Need for Cognition",
        102: "Need for Cognition", 
        103: "Need for Cognition",
        104: "Need for Cognition",
        105: "Need for Cognition",
        201: "Actively Open-Minded Thinking",
        202: "Actively Open-Minded Thinking", 
        203: "Actively Open-Minded Thinking",
        204: "Actively Open-Minded Thinking",
        205: "Actively Open-Minded Thinking",
        301: "Epistemic Curiosity",
        302: "Epistemic Curiosity",
        303: "Epistemic Curiosity", 
        304: "Epistemic Curiosity",
        305: "Epistemic Curiosity",
        401: "Tolerance for Ambiguity",
        402: "Tolerance for Ambiguity",
        403: "Tolerance for Ambiguity",
        404: "Tolerance for Ambiguity", 
        405: "Tolerance for Ambiguity",
        501: "Intellectual Humility",
        502: "Intellectual Humility",
        503: "Intellectual Humility",
        504: "Intellectual Humility",
        505: "Intellectual Humility",
        601: "Trait Emotional Intelligence",
        602: "Trait Emotional Intelligence",
        603: "Trait Emotional Intelligence",
        604: "Trait Emotional Intelligence",
        605: "Trait Emotional Intelligence",
        701: "Holistic Thinking Preference",
        702: "Holistic Thinking Preference",
        703: "Holistic Thinking Preference",
        704: "Holistic Thinking Preference",
        705: "Holistic Thinking Preference",
        801: "Experimental Drive",
        802: "Experimental Drive",
        803: "Experimental Drive",
        804: "Experimental Drive",
        805: "Experimental Drive",
        901: "Deliberative Stance",
        902: "Deliberative Stance",
        903: "Deliberative Stance",
        904: "Deliberative Stance",
        905: "Deliberative Stance",
        1001: "Principled Ethics Orientation",
        1002: "Principled Ethics Orientation",
        1003: "Principled Ethics Orientation",
        1004: "Principled Ethics Orientation",
        1005: "Principled Ethics Orientation",
        1101: "General Trust Propensity",
        1102: "General Trust Propensity",
        1103: "General Trust Propensity",
        1104: "General Trust Propensity",
        1105: "General Trust Propensity"
    }

def create_fallback_report(nickname, primary_archetype, secondary_archetype):
    """Create a comprehensive report for testing"""
    
    return f"""# Your AI Navigator Profile

**Nickname:** {nickname}

### Executive Summary

Your assessment results show a strong profile as a {primary_archetype['name']}, with complementary strengths from {secondary_archetype['name'] if secondary_archetype else 'your other traits'}. This combination gives you a unique approach to AI navigation work that balances analytical thinking with practical application.

---

### Your Primary Archetype: {primary_archetype['name']}

This archetype represents your dominant approach to AI navigation work. Your scores indicate natural strengths in this area.

**Signature Strengths:**
* Strong analytical and systematic thinking
* Excellent problem-solving abilities
* High standards for quality and precision
* Ability to break down complex problems
* Systematic approach to decision-making

**Potential Blind Spots:**
* May over-analyze simple situations
* Could miss intuitive or creative solutions
* Risk of analysis paralysis
* May overlook human factors
* Could be perceived as overly critical

---

### Developmental Opportunities

* **To enhance your {primary_archetype['name']} style:** Focus on balancing analysis with action, and consider the human impact of your decisions. Practice making decisions with incomplete information when appropriate.

* **To leverage your {secondary_archetype['name'] if secondary_archetype else 'other'} strengths:** Integrate complementary approaches to create more well-rounded solutions. Consider how your secondary archetype's strengths can complement your primary approach.

---

### Detailed Trait Scores

Your assessment measured 11 core constructs that contribute to effective AI navigation. Your scores reflect your natural preferences and tendencies in these areas:

* **Need for Cognition:** Your preference for complex mental tasks
* **Actively Open-Minded Thinking:** Your willingness to consider alternative viewpoints
* **Epistemic Curiosity:** Your desire to learn and explore new information
* **Tolerance for Ambiguity:** Your comfort with uncertainty and unclear situations
* **Intellectual Humility:** Your awareness of your own knowledge limitations
* **Trait Emotional Intelligence:** Your ability to understand and work with emotions
* **Holistic Thinking Preference:** Your tendency to see the big picture
* **Experimental Drive:** Your willingness to try new approaches
* **Deliberative Stance:** Your preference for careful consideration
* **Principled Ethics Orientation:** Your commitment to ethical decision-making
* **General Trust Propensity:** Your natural tendency to trust others

---

**Remember:** This profile reflects your natural tendencies and preferences. Use these insights to understand your strengths and identify areas for growth. Every archetype brings valuable perspectives to AI navigation work.

Your unique combination of traits makes you well-suited for AI navigation challenges that require both analytical rigor and practical application. Focus on leveraging your strengths while developing complementary skills to become a more well-rounded AI navigator.
""" 