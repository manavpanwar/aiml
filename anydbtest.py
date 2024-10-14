import warnings
from sqlalchemy import create_engine, MetaData
import requests
from langchain.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

# Suppress specific deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Initialize Ollama instance with your model server details
OLLAMA_URL = "http://122.176.146.28:11434"  # Update the port if necessary
MODEL_NAME = "test14"  # Replace with your actual model name for your Ollama instance
ollama_instance = Ollama(base_url=OLLAMA_URL, model=MODEL_NAME)

def connect_to_database(database_url):
    """Connect to the database and return the engine."""
    engine = create_engine(database_url)
    return engine

def retrieve_documents(engine, table_name, query):
    """Retrieve relevant documents from the specified table based on the user query."""
    documents = []
    metadata = MetaData()
    metadata.reflect(bind=engine)  # Reflect the tables in the engine
    table = metadata.tables[table_name]

    # Print the column names of the selected table
    print(f"Columns in '{table_name}':", table.columns.keys())

    # Create a connection to execute the query
    with engine.connect() as connection:
        # Ask the user to specify a column name to search in
        column_name = input("Enter the column name to search (as shown above): ").strip()

        if column_name not in table.columns:
            print(f"Column '{column_name}' does not exist in table '{table_name}'.")
            return []

        # Search using regex on the specified field
        results = connection.execute(table.select().where(table.c[column_name].like(f"%{query}%")))
        documents.extend([dict(row) for row in results])

    return documents

def check_llm_status():
    """Check if the Ollama LLM is online."""
    try:
        response = requests.get(f"{OLLAMA_URL}/status")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error checking LLM status: {e}")
        return False

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
    database_url = input("Enter your database URL (e.g., mysql+pymysql://user:password@host:port/dbname): ")
    user_query = input("Enter your query: ")  # Get user input
    engine = connect_to_database(database_url)

    # Check if the LLM is online
    if not check_llm_status():
        print("LLM is offline. Please check the server status.")
        return

    # Get all tables in the database
    metadata = MetaData()
    metadata.reflect(bind=engine)
    tables = metadata.tables.keys()
    print("Fetched Tables:", tables)

    # Let the user select a table
    table_name = input("Enter the table name to work with: ").strip()
    if table_name not in tables:
        print(f"Table '{table_name}' does not exist.")
        return

    retrieved_docs = retrieve_documents(engine, table_name, user_query)  # Retrieve relevant documents from the selected table

    if retrieved_docs:
        response = generate_response(user_query, retrieved_docs)  # Generate response
        print("Generated Response:", response)
    else:
        print("No relevant documents found.")

if __name__ == "__main__":
    main()
