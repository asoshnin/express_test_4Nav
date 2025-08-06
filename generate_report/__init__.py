import azure.functions as func
import logging
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List

# Azure SDK imports
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from openai import AzureOpenAI

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Generate Report API - Creates personalized assessment report using GPT-4
    
    GET /api/assessment/{sessionId}/report
    Returns: 200 OK with report data or 410 if already viewed
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
        
        # Check if assessment is completed
        if session.get('status') != 'Completed':
            return func.HttpResponse(
                json.dumps({"error": "Assessment not completed"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Check if report has already been viewed
        if session.get('reportFirstViewedAt'):
            return func.HttpResponse(
                json.dumps({"error": "Report already viewed"}),
                status_code=410,
                mimetype="application/json"
            )
        
        # Calculate scores and generate report
        result = calculate_scores_and_generate_report(session)
        
        # Update session with report data and mark as viewed
        update_session_with_report(cosmos_client_instance, session_id, result)
        
        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error in generate_report: {str(e)}")
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
    
    # Generate personalized report using GPT-4
    report_content = generate_personalized_report(
        nickname, construct_scores, archetype_scores, primary_archetype, secondary_archetype
    )
    
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

def generate_personalized_report(nickname, construct_scores, archetype_scores, primary_archetype, secondary_archetype):
    """Generate personalized report using GPT-4"""
    
    try:
        # Initialize Azure OpenAI client
        client = AzureOpenAI(
            azure_endpoint=os.environ.get('AZURE_OPENAI_ENDPOINT'),
            api_key=os.environ.get('AZURE_OPENAI_KEY'),
            api_version="2024-02-15-preview"
        )
        
        # Prepare the prompt for GPT-4
        prompt = create_report_generation_prompt(
            nickname, construct_scores, archetype_scores, primary_archetype, secondary_archetype
        )
        
        # Generate report using GPT-4
        response = client.chat.completions.create(
            model=os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME_GPT4'),
            messages=[
                {"role": "system", "content": "You are an expert psychometrician and career development specialist. Generate personalized, empowering reports based on assessment data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f"Error generating report with GPT-4: {str(e)}")
        # Fallback to a basic report
        return create_fallback_report(nickname, primary_archetype, secondary_archetype)

def create_report_generation_prompt(nickname, construct_scores, archetype_scores, primary_archetype, secondary_archetype):
    """Create the prompt for GPT-4 report generation"""
    
    # Archetype descriptions from the Knowledge Base
    archetype_descriptions = {
        "The Critical Interrogator": {
            "description": "You excel at rigorous analysis and systematic thinking. You naturally question assumptions, seek evidence, and build robust arguments. Your strength lies in breaking down complex problems into manageable components and evaluating information critically.",
            "strengths": [
                "Exceptional analytical thinking and logical reasoning",
                "Strong ability to identify flaws in arguments and assumptions",
                "Systematic approach to problem-solving",
                "High standards for evidence and proof",
                "Excellent attention to detail and precision"
            ],
            "blind_spots": [
                "May over-analyze simple situations",
                "Can be perceived as overly critical or skeptical",
                "May miss intuitive or creative solutions",
                "Could overlook emotional or human factors",
                "Risk of analysis paralysis in time-sensitive situations"
            ]
        },
        "The Human-Centric Strategist": {
            "description": "You naturally understand and work with human dynamics, emotional intelligence, and ethical considerations. You excel at building trust, fostering collaboration, and considering the broader impact of decisions on people and systems.",
            "strengths": [
                "Strong emotional intelligence and people skills",
                "Ability to build trust and foster collaboration",
                "Holistic understanding of human dynamics",
                "Strong ethical compass and principled decision-making",
                "Natural ability to see the big picture"
            ],
            "blind_spots": [
                "May prioritize relationships over necessary conflict",
                "Could overlook technical or analytical details",
                "Risk of being overly trusting or optimistic",
                "May avoid difficult but necessary decisions",
                "Could miss opportunities for efficiency or optimization"
            ]
        },
        "The Curious Experimenter": {
            "description": "You thrive on exploration, experimentation, and learning through hands-on experience. You're comfortable with uncertainty and enjoy trying new approaches to solve problems. Your strength lies in rapid prototyping and iterative improvement.",
            "strengths": [
                "Natural curiosity and love of learning",
                "Comfort with uncertainty and ambiguity",
                "Strong experimental and hands-on approach",
                "Ability to quickly adapt and iterate",
                "Openness to new ideas and perspectives"
            ],
            "blind_spots": [
                "May lack systematic planning and follow-through",
                "Could jump between projects without completion",
                "Risk of being scattered or unfocused",
                "May overlook established best practices",
                "Could underestimate the importance of stability"
            ]
        }
    }
    
    prompt = f"""
Generate a personalized AI Navigator Profile report for the user with nickname "{nickname}".

Assessment Results:
- Primary Archetype: {primary_archetype['name']} (Score: {primary_archetype['score']}, Percentile: {primary_archetype['percentile']})
- Secondary Archetype: {secondary_archetype['name'] if secondary_archetype else 'None'} (Score: {secondary_archetype['score'] if secondary_archetype else 'N/A'}, Percentile: {secondary_archetype['percentile'] if secondary_archetype else 'N/A'})

Construct Scores:
{chr(10).join([f"- {score['name']}: {score['score']} (Percentile: {score['percentile']})" for score in construct_scores])}

Archetype Information:
{chr(10).join([f"## {archetype['name']}{chr(10)}{archetype_descriptions[archetype['name']]['description']}{chr(10)}**Strengths:**{chr(10)}{chr(10).join([f'- {strength}' for strength in archetype_descriptions[archetype['name']]['strengths']])}{chr(10)}**Potential Blind Spots:**{chr(10)}{chr(10).join([f'- {blind_spot}' for blind_spot in archetype_descriptions[archetype['name']]['blind_spots']])}" for archetype in [primary_archetype, secondary_archetype] if archetype])}

Please generate a comprehensive, empowering report using this Markdown template:

# Your AI Navigator Profile

**Nickname:** {nickname}

### Executive Summary

[Generate 2-3 sentences of nuanced interpretation based on the user's mix of primary and secondary archetypes. Be empowering and constructive.]

---

### Your Primary Archetype: {primary_archetype['name']}

[Use the description provided above, but personalize it based on the user's specific scores and profile.]

**Signature Strengths:**
[Adapt the strengths list to be more personalized based on the user's specific construct scores.]

**Potential Blind Spots:**
[Adapt the blind spots list to be more personalized and constructive.]

---

### Developmental Opportunities

* **To enhance your {primary_archetype['name']} style:** [Provide 1-2 sentences of actionable advice based on the archetype's blind spots.]
* **To leverage your {secondary_archetype['name'] if secondary_archetype else 'other'} strengths:** [Provide 1-2 sentences of actionable advice on how to integrate the secondary archetype's strengths.]

---

### Detailed Trait Scores

The following shows your percentile scores across the 11 core constructs:

{chr(10).join([f"**{score['name']}:** {score['percentile']}th percentile" for score in construct_scores])}

---

**Remember:** This profile reflects your natural tendencies and preferences. Use these insights to understand your strengths and identify areas for growth. Every archetype brings valuable perspectives to AI navigation work.
"""
    
    return prompt

def create_fallback_report(nickname, primary_archetype, secondary_archetype):
    """Create a basic fallback report if GPT-4 is unavailable"""
    
    return f"""# Your AI Navigator Profile

**Nickname:** {nickname}

### Executive Summary

Your assessment results show a strong profile as a {primary_archetype['name']}, with complementary strengths from {secondary_archetype['name'] if secondary_archetype else 'your other traits'}.

---

### Your Primary Archetype: {primary_archetype['name']}

This archetype represents your dominant approach to AI navigation work. Your scores indicate natural strengths in this area.

**Signature Strengths:**
* Strong analytical and systematic thinking
* Excellent problem-solving abilities
* High standards for quality and precision

**Potential Blind Spots:**
* May over-analyze simple situations
* Could miss intuitive or creative solutions
* Risk of analysis paralysis

---

### Developmental Opportunities

* **To enhance your {primary_archetype['name']} style:** Focus on balancing analysis with action, and consider the human impact of your decisions.
* **To leverage your {secondary_archetype['name'] if secondary_archetype else 'other'} strengths:** Integrate complementary approaches to create more well-rounded solutions.

---

### Detailed Trait Scores

Your assessment measured 11 core constructs that contribute to effective AI navigation. Your scores reflect your natural preferences and tendencies in these areas.

---

**Note:** This is a basic report. For a more detailed, personalized analysis, please try again later when the AI report generation service is available.
"""

def update_session_with_report(cosmos_client_instance, session_id, result):
    """Update session with report data and mark as viewed"""
    try:
        database_name = get_database_name()
        container_name = get_container_name()
        container = cosmos_client_instance.get_database_client(database_name).get_container_client(container_name)
        
        # Get current session
        session = get_session(cosmos_client_instance, session_id)
        if not session:
            raise ValueError("Session not found for update")
        
        # Update session with report data
        session['result'] = result
        session['reportFirstViewedAt'] = datetime.now(timezone.utc).isoformat()
        
        # Replace the document
        container.replace_item(item=session_id, body=session)
        
        logging.info(f"Session {session_id} updated with report data")
        
    except Exception as e:
        logging.error(f"Error updating session with report: {str(e)}")
        raise 