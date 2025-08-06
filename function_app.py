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

# Register the session_cleanup function
@app.function_name(name="session_cleanup")
@app.route(route="api/admin/sessions/cleanup", methods=["DELETE"])
def session_cleanup(req: func.HttpRequest) -> func.HttpResponse:
    return session_cleanup_main(req)

# Register the session_reset function
@app.function_name(name="session_reset")
@app.route(route="api/admin/sessions/{sessionId}/reset", methods=["POST"])
def session_reset(req: func.HttpRequest) -> func.HttpResponse:
    return session_reset_main(req)