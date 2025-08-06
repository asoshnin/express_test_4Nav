import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

# Import the start_assessment function
from start_assessment import main as start_assessment_main

# Import the get_question function
from get_question import main as get_question_main

# Import the submit_answer function
from submit_answer import main as submit_answer_main

# Import the generate_report function
from generate_report import main as generate_report_main

# Import the contact function
from contact import main as contact_main

# Import the admin function
from admin import main as admin_main

# Import the download_report function
from download_report import main as download_report_main

# Import the health function
from health import main as health_main

# Import the session_status function
from session_status import main as session_status_main

# Import the analytics function
from analytics import main as analytics_main

# Register the start_assessment function
@app.function_name(name="start_assessment")
@app.route(route="assessment", methods=["POST"])
def start_assessment(req: func.HttpRequest) -> func.HttpResponse:
    return start_assessment_main(req)

# Register the get_question function
@app.function_name(name="get_question")
@app.route(route="assessment/{sessionId}/question", methods=["GET"])
def get_question(req: func.HttpRequest) -> func.HttpResponse:
    return get_question_main(req)

# Register the submit_answer function
@app.function_name(name="submit_answer")
@app.route(route="assessment/{sessionId}/answer", methods=["POST"])
def submit_answer(req: func.HttpRequest) -> func.HttpResponse:
    return submit_answer_main(req)

# Register the generate_report function
@app.function_name(name="generate_report")
@app.route(route="assessment/{sessionId}/report", methods=["GET"])
def generate_report(req: func.HttpRequest) -> func.HttpResponse:
    return generate_report_main(req)

# Register the download_report function
@app.function_name(name="download_report")
@app.route(route="assessment/{sessionId}/report/download", methods=["GET"])
def download_report(req: func.HttpRequest) -> func.HttpResponse:
    return download_report_main(req)

# Register the health function
@app.function_name(name="health")
@app.route(route="health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    return health_main(req)

# Register the session_status function
@app.function_name(name="session_status")
@app.route(route="assessment/{sessionId}/status", methods=["GET"])
def session_status(req: func.HttpRequest) -> func.HttpResponse:
    return session_status_main(req)

# Register the analytics function
@app.function_name(name="analytics")
@app.route(route="analytics", methods=["GET"])
def analytics(req: func.HttpRequest) -> func.HttpResponse:
    return analytics_main(req)

# Register the contact function
@app.function_name(name="contact")
@app.route(route="assessment/{sessionId}/contact", methods=["POST"])
def contact(req: func.HttpRequest) -> func.HttpResponse:
    return contact_main(req)

# Register the admin function
@app.function_name(name="admin")
@app.route(route="api/admin/assessments", methods=["GET"])
def admin(req: func.HttpRequest) -> func.HttpResponse:
    return admin_main(req)