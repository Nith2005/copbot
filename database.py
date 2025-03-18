import pandas as pd

# Load police data from CSV file
def load_data():
    """Loads police queries and responses from a CSV file."""
    try:
        data = pd.read_csv("police_data.csv")
        return dict(zip(data["query"].str.lower(), data["response"]))
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return {}

# Load the dataset into memory
police_data = load_data()

def get_response(query):
    """Finds the best response for a given query."""
    query_lower = query.lower()
    
    for key in police_data:
        if key in query_lower:
            return police_data[key]

    return "I'm sorry, I couldn't understand your query. Please visit the nearest police station for more information."
