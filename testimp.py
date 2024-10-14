import warnings
import mysql.connector
from langchain.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Suppress specific deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)

# MySQL Database Connection
def get_database_connection():
    try:
        connection = mysql.connector.connect(
            host='122.176.146.28',        # Replace with your MySQL host
            user='mysql',                 # Replace with your MySQL username
            password='Samepassword1!',    # Replace with your MySQL password
            database='csv_upload'         # Replace with your database name
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to get table schema for LLM
def get_table_schema(table_name):
    connection = get_database_connection()
    if connection is None:
        return "Unable to connect to the database."

    cursor = connection.cursor()
    query = f"DESCRIBE {table_name};"  # Get table schema
    cursor.execute(query)
    columns = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    
    # Return columns as a comma-separated string
    return ", ".join(columns)

# Function to generate SQL query using Ollama for SQL tasks
def generate_sql_query(user_input, table_name, sql_ollama_instance):
    # Get the table schema
    table_schema = get_table_schema(table_name)
    
    if "Unable to connect" in table_schema:
        return table_schema

    # Create a prompt to ask Ollama to generate an SQL query
    query_prompt = f"""
    You are an expert SQL query generator. The table '{table_name}' has the following columns: {table_schema}.
    Based on the user's request: '{user_input}', generate an SQL query that fetches the relevant data from the table.
    """
    
    # Use the SQL Ollama instance to generate the query
    response = sql_ollama_instance.generate(prompts=[query_prompt])
    
    # Extract the generated SQL query from the response
    generated_query = response['text'].strip()
    
    return generated_query

# Function to fetch relevant data using the generated query
def fetch_data_using_generated_query(user_input, table_name, sql_ollama_instance):
    connection = get_database_connection()
    if connection is None:
        return "Unable to connect to the database."

    # Use Ollama to generate the SQL query
    generated_query = generate_sql_query(user_input, table_name, sql_ollama_instance)
    
    if "Unable to connect" in generated_query:
        return generated_query
    
    # Print the generated query (for debugging purposes)
    print("Generated Query: ", generated_query)
    
    cursor = connection.cursor()
    try:
        cursor.execute(generated_query)
        results = cursor.fetchall()
        formatted_results = "\n".join([str(row) for row in results])
    except mysql.connector.Error as err:
        formatted_results = f"Error executing query: {err}"
    
    cursor.close()
    connection.close()
    
    return formatted_results if formatted_results else "No relevant data found."

# Initialize Ollama instance for SQL query generation
sql_ollama_instance = Ollama(base_url="http://122.176.146.28:11434", model="nlpsql")

# Prompt template for chatbot responses
template = """You are a helpful assistant with access to a database.
The conversation history is:
{history}

User: {input}
Here is some relevant data from the table '{table_name}':
{knowledge}
Assistant:"""

prompt = PromptTemplate(
    input_variables=["history", "input", "knowledge", "table_name"],
    template=template,
)

# Langchain memory to store the conversation context
memory = ConversationBufferMemory()

# Initialize Ollama instance for chatbot responses
chatbot_ollama_instance = Ollama(base_url="http://122.176.146.28:11434", model="test14")

# Define the LLMChain with Ollama for chatbot responses
conversation_chain = LLMChain(
    llm=chatbot_ollama_instance,
    prompt=prompt,
    memory=memory,
)

# Chatbot loop
print("Chatbot: Hi! How can I assist you today?")
while True:
    user_input = input("User: ")
    
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break
    
    table_name = "superstore"  # Use the appropriate table name
    
    # Fetch data based on the generated SQL query
    relevant_data = fetch_data_using_generated_query(user_input, table_name, sql_ollama_instance)

    # Generate a response using the chatbot's conversation chain
    response = conversation_chain.invoke({
        "input": user_input,
        "knowledge": relevant_data,
        "history": memory.buffer,
        "table_name": table_name  # Pass the table name as input
    })

    print(f"Chatbot: {response}")
