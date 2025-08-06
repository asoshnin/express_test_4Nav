import azure.functions as func
import logging
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any
from shared_session_storage import get_session

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Report Download API - Provides downloadable Markdown report
    
    GET /api/assessment/{sessionId}/report/download
    Returns: 200 OK with Markdown file or 404 if session not found
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

        # Get session from shared storage
        session = get_session(session_id)
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

        # Check if report exists
        if not session.get('result'):
            return func.HttpResponse(
                json.dumps({"error": "Report not generated"}),
                status_code=400,
                mimetype="application/json"
            )

        # Generate Markdown content
        markdown_content = generate_markdown_report(session)

        # Create filename with nickname
        nickname = session.get('nickname', 'Unknown')
        filename = f"navigator-report-{nickname}.md"

        # Return Markdown file
        return func.HttpResponse(
            markdown_content,
            status_code=200,
            mimetype="text/markdown",
            headers={
                "Content-Disposition": f"attachment; filename=\"{filename}\"",
                "Cache-Control": "no-cache"
            }
        )

    except Exception as e:
        logging.error(f"Error in download_report: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )

def generate_markdown_report(session):
    """Generate Markdown report content from session data"""
    
    nickname = session.get('nickname', 'Unknown')
    result = session.get('result', {})
    completed_at = session.get('completedAt', 'Unknown')
    
    # Format completion date
    try:
        completed_date = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
        formatted_date = completed_date.strftime("%B %d, %Y at %I:%M %p UTC")
    except:
        formatted_date = completed_at

    # Extract report data
    primary_archetype = result.get('primaryArchetype', 'Unknown')
    secondary_archetype = result.get('secondaryArchetype')
    report_content = result.get('reportContent', '')
    
    # Get scores
    archetype_scores = result.get('scores', {}).get('archetypes', [])
    construct_scores = result.get('scores', {}).get('constructs', [])

    # Generate Markdown content
    markdown = f"""# AI Navigator Profile Report

**Nickname:** {nickname}  
**Assessment Completed:** {formatted_date}

---

## Executive Summary

This report presents your AI Navigator Profile based on your responses to 40 carefully designed questions. Your profile reveals your natural tendencies and preferences when working with AI systems and navigating complex technological environments.

---

## Your Primary Archetype: {primary_archetype}

{get_archetype_description(primary_archetype)}

### Signature Strengths

{get_archetype_strengths(primary_archetype)}

### Potential Blind Spots

{get_archetype_blind_spots(primary_archetype)}

"""

    # Add secondary archetype if present
    if secondary_archetype:
        markdown += f"""
## Your Secondary Archetype: {secondary_archetype}

{get_archetype_description(secondary_archetype)}

### Complementary Strengths

{get_archetype_strengths(secondary_archetype)}

### Integration Opportunities

{get_archetype_integration_opportunities(secondary_archetype)}

"""

    # Add detailed scores
    markdown += f"""
## Detailed Assessment Scores

### Archetype Scores

"""
    
    for score in archetype_scores:
        markdown += f"- **{score['name']}:** {score['score']} points ({score['percentile']}th percentile)\n"

    markdown += f"""
### Construct Scores

The following shows your percentile scores across the 11 core constructs that contribute to effective AI navigation:

"""
    
    for score in construct_scores:
        markdown += f"- **{score['name']}:** {score['percentile']}th percentile\n"

    # Add personalized report content if available
    if report_content:
        markdown += f"""
---

## Personalized Insights

{report_content}

"""

    # Add footer
    markdown += f"""
---

## About This Assessment

This AI Navigator Profile was generated using a scientifically-grounded psychometric framework designed to identify the core traits of successful AI navigators. The assessment measures 11 key constructs across three primary archetypes:

- **The Critical Interrogator:** Analytical thinking and systematic problem-solving
- **The Human-Centric Strategist:** Emotional intelligence and ethical decision-making  
- **The Curious Experimenter:** Adaptability and hands-on learning

Your results reflect your natural preferences and tendencies. Remember that every archetype brings valuable perspectives to AI navigation work, and your unique combination of traits creates your distinctive approach.

---

**Report Generated:** {datetime.now(timezone.utc).strftime("%B %d, %Y at %I:%M %p UTC")}  
**Assessment ID:** {session.get('id', 'Unknown')}
"""

    return markdown

def get_archetype_description(archetype_name):
    """Get description for an archetype"""
    descriptions = {
        "The Critical Interrogator": "You excel at rigorous analysis and systematic thinking. You naturally question assumptions, seek evidence, and build robust arguments. Your strength lies in breaking down complex problems into manageable components and evaluating information critically.",
        "The Human-Centric Strategist": "You naturally understand and work with human dynamics, emotional intelligence, and ethical considerations. You excel at building trust, fostering collaboration, and considering the broader impact of decisions on people and systems.",
        "The Curious Experimenter": "You thrive on exploration, experimentation, and learning through hands-on experience. You're comfortable with uncertainty and enjoy trying new approaches to solve problems. Your strength lies in rapid prototyping and iterative improvement."
    }
    return descriptions.get(archetype_name, f"{archetype_name} represents your dominant approach to AI navigation work.")

def get_archetype_strengths(archetype_name):
    """Get strengths for an archetype"""
    strengths = {
        "The Critical Interrogator": [
            "Exceptional analytical thinking and logical reasoning",
            "Strong ability to identify flaws in arguments and assumptions",
            "Systematic approach to problem-solving",
            "High standards for evidence and proof",
            "Excellent attention to detail and precision"
        ],
        "The Human-Centric Strategist": [
            "Strong emotional intelligence and people skills",
            "Ability to build trust and foster collaboration",
            "Holistic understanding of human dynamics",
            "Strong ethical compass and principled decision-making",
            "Natural ability to see the big picture"
        ],
        "The Curious Experimenter": [
            "Natural curiosity and love of learning",
            "Comfort with uncertainty and ambiguity",
            "Strong experimental and hands-on approach",
            "Ability to quickly adapt and iterate",
            "Openness to new ideas and perspectives"
        ]
    }
    
    strength_list = strengths.get(archetype_name, ["Strong analytical capabilities", "Effective problem-solving approach"])
    return "\n".join([f"- {strength}" for strength in strength_list])

def get_archetype_blind_spots(archetype_name):
    """Get blind spots for an archetype"""
    blind_spots = {
        "The Critical Interrogator": [
            "May over-analyze simple situations",
            "Can be perceived as overly critical or skeptical",
            "May miss intuitive or creative solutions",
            "Could overlook emotional or human factors",
            "Risk of analysis paralysis in time-sensitive situations"
        ],
        "The Human-Centric Strategist": [
            "May prioritize relationships over necessary conflict",
            "Could overlook technical or analytical details",
            "Risk of being overly trusting or optimistic",
            "May avoid difficult but necessary decisions",
            "Could miss opportunities for efficiency or optimization"
        ],
        "The Curious Experimenter": [
            "May lack systematic planning and follow-through",
            "Could jump between projects without completion",
            "Risk of being scattered or unfocused",
            "May overlook established best practices",
            "Could underestimate the importance of stability"
        ]
    }
    
    blind_spot_list = blind_spots.get(archetype_name, ["May need to balance different approaches", "Consider complementary perspectives"])
    return "\n".join([f"- {blind_spot}" for blind_spot in blind_spot_list])

def get_archetype_integration_opportunities(archetype_name):
    """Get integration opportunities for secondary archetype"""
    opportunities = {
        "The Critical Interrogator": [
            "Use analytical skills to evaluate human dynamics more systematically",
            "Apply logical frameworks to ethical decision-making",
            "Balance rigor with empathy in collaborative settings"
        ],
        "The Human-Centric Strategist": [
            "Leverage emotional intelligence to enhance analytical processes",
            "Use collaborative skills to improve experimental approaches",
            "Apply ethical frameworks to experimental decision-making"
        ],
        "The Curious Experimenter": [
            "Channel curiosity into more systematic exploration",
            "Use experimental mindset to enhance analytical creativity",
            "Apply hands-on learning to improve human-centric approaches"
        ]
    }
    
    opportunity_list = opportunities.get(archetype_name, [
        "Integrate complementary approaches to create well-rounded solutions",
        "Balance different perspectives for optimal outcomes"
    ])
    return "\n".join([f"- {opportunity}" for opportunity in opportunity_list]) 