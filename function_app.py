import azure.functions as func

# Import all function modules
from start_assessment import main as start_assessment_main
from get_question import main as get_question_main
from submit_answer import main as submit_answer_main
from generate_report import main as generate_report_main
from contact import main as contact_main
from admin import main as admin_main
from download_report import main as download_report_main
from health import main as health_main
from session_status import main as session_status_main
from analytics import main as analytics_main
from session_cleanup import main as session_cleanup_main
from session_reset import main as session_reset_main

app = func.FunctionApp()

def add_cors_headers(response: func.HttpResponse) -> func.HttpResponse:
    """Add CORS headers to the response"""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# Register the start_assessment function
@app.function_name(name="start_assessment")
@app.route(route="assessment", methods=["POST"])
def start_assessment(req: func.HttpRequest) -> func.HttpResponse:
    response = start_assessment_main(req)
    return add_cors_headers(response)

# Register the get_question function
@app.function_name(name="get_question")
@app.route(route="assessment/{sessionId}/question", methods=["GET"])
def get_question(req: func.HttpRequest) -> func.HttpResponse:
    response = get_question_main(req)
    return add_cors_headers(response)

# Register the submit_answer function
@app.function_name(name="submit_answer")
@app.route(route="assessment/{sessionId}/answer", methods=["POST"])
def submit_answer(req: func.HttpRequest) -> func.HttpResponse:
    response = submit_answer_main(req)
    return add_cors_headers(response)

# Register the submit_answers_batch function
@app.function_name(name="submit_answers_batch")
@app.route(route="assessment/{sessionId}/answers", methods=["POST"])
def submit_answers_batch(req: func.HttpRequest) -> func.HttpResponse:
    from submit_answers_batch import main as submit_answers_batch_main
    response = submit_answers_batch_main(req)
    return add_cors_headers(response)

# Register the generate_report function
@app.function_name(name="generate_report")
@app.route(route="assessment/{sessionId}/report", methods=["GET"])
def generate_report(req: func.HttpRequest) -> func.HttpResponse:
    response = generate_report_main(req)
    return add_cors_headers(response)

# Register the download_report function
@app.function_name(name="download_report")
@app.route(route="assessment/{sessionId}/report/download", methods=["GET"])
def download_report(req: func.HttpRequest) -> func.HttpResponse:
    response = download_report_main(req)
    return add_cors_headers(response)

# Register the health function
@app.function_name(name="health")
@app.route(route="health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    response = health_main(req)
    return add_cors_headers(response)

# Register the session_status function
@app.function_name(name="session_status")
@app.route(route="assessment/{sessionId}/status", methods=["GET"])
def session_status(req: func.HttpRequest) -> func.HttpResponse:
    response = session_status_main(req)
    return add_cors_headers(response)

# Register the analytics function
@app.function_name(name="analytics")
@app.route(route="analytics", methods=["GET"])
def analytics(req: func.HttpRequest) -> func.HttpResponse:
    response = analytics_main(req)
    return add_cors_headers(response)

# Register the contact function
@app.function_name(name="contact")
@app.route(route="assessment/{sessionId}/contact", methods=["POST"])
def contact(req: func.HttpRequest) -> func.HttpResponse:
    response = contact_main(req)
    return add_cors_headers(response)

# Register the admin function
@app.function_name(name="admin")
@app.route(route="api/admin/assessments", methods=["GET"])
def admin(req: func.HttpRequest) -> func.HttpResponse:
    response = admin_main(req)
    return add_cors_headers(response)

# Register the session_cleanup function
@app.function_name(name="session_cleanup")
@app.route(route="api/admin/sessions/cleanup", methods=["DELETE"])
def session_cleanup(req: func.HttpRequest) -> func.HttpResponse:
    response = session_cleanup_main(req)
    return add_cors_headers(response)

# Register the session_reset function
@app.function_name(name="session_reset")
@app.route(route="api/admin/sessions/{sessionId}/reset", methods=["POST"])
def session_reset(req: func.HttpRequest) -> func.HttpResponse:
    response = session_reset_main(req)
    return add_cors_headers(response)