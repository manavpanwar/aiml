import pymongo
import requests

# MongoDB configuration
MONGODB_URI = "mongodb+srv://prince961:XRcDfeLA6foxoWtz@cluster0.ox5zuer.mongodb.net/CompanyDB?retryWrites=true&w=majority"  # Your MongoDB URI
DATABASE_NAME = "CompanyDB"  # Replace with your database name

# Ollama local instance URL
OLLAMA_URL = "http://122.176.146.28:11434"  # Update the port if necessary
MODEL_NAME = "test14"  # Replace with your actual model name for your Ollama instance

def connect_to_mongodb():
    """Connect to MongoDB and return the client and database."""
    client = pymongo.MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    return client, db

def retrieve_documents(query):
    """Retrieve relevant documents from all collections based on the user query."""
    client, db = connect_to_mongodb()
    documents = []

    # Loop through all collections in the database
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        
        # Search using regex on specified fields
        results = collection.find({"$or": [{"title": {"$regex": query, "$options": "i"}},
                                            {"description": {"$regex": query, "$options": "i"}},
                                           ]})
        
        documents.extend([doc for doc in results])  # Add retrieved docs to the list

    client.close()
    return documents

def generate_response(user_query, retrieved_docs):
    """Generate a response using the specified Ollama model with the user query and retrieved documents."""
    context = "\n".join([doc['description'] for doc in retrieved_docs])  # Assuming documents have a 'description' field
    prompt = (
        "You are an expert in organizing pivot tables. Your task is to assist users in arranging data from the superstore sample database into rows, columns, values, and filters for effective analysis. "
        "The available fields include: Row ID, Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Customer Name, Segment, Country, City, State, Postal Code, Region, Product ID, Category, Sub-Category, Product Name, Sales, Quantity, Discount, Profit, and Zone.\n\n"
        f"When a user sends a request: '{user_query}', analyze it to identify the relevant fields based on the context and provide a response in JSON format."
    )

    payload = {
        "prompt": prompt,
        "max_tokens": 300,  # Adjust as needed
        "model": MODEL_NAME  # Specify your model name here
    }

    response = requests.post(f"{OLLAMA_URL}/generate", json=payload)
    if response.status_code == 200:
        return response.json()['response']
    else:
        return "Error generating response."

def main():
    user_query = input("Enter your query: ")  # Get user input
    retrieved_docs = retrieve_documents(user_query)  # Retrieve relevant documents from all collections

    if retrieved_docs:
        response = generate_response(user_query, retrieved_docs)  # Generate response
        print("Generated Response:", response)
    else:
        print("No relevant documents found.")

if __name__ == "__main__":
    main()
