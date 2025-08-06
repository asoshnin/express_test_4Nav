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