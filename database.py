# Simulated police data (replace with actual database or file read logic)
police_data = {
    "FIR": "To file an FIR, visit the nearest police station with a valid ID.",
    "complaint": "You can file a complaint at the police station or online.",
    "investigation": "After an FIR, police collect evidence and interview witnesses.",
    "emergency": "Dial 112 for immediate police assistance.",
    "law": "Refer to local law books or visit the police station for legal information.",
    "default": "I'm sorry, I couldn't understand your query. Please contact the police station."
}

def get_response(query):
    """Returns a response based on user query."""
    query_lower = query.lower()
    for key in police_data:
        if key in query_lower:
            return police_data[key]
    return police_data["default"]
