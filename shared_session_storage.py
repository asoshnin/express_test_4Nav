# Shared session storage for testing
# In production, this would be stored in Cosmos DB

session_storage = {}

def get_session(session_id):
    """Get or create a session"""
    if session_id not in session_storage:
        session_storage[session_id] = {
            "id": session_id,
            "answers": [],
            "status": "InProgress"
        }
    return session_storage[session_id]

def update_session(session):
    """Update a session"""
    session_storage[session["id"]] = session 