from langchain.llms import Ollama
import pandas as pd
import requests# Import the requests library

# Initialize context for Ollama
context = """
You are a pivot table expert. You need to organize data fields into rows, values, filters, and columns. Your database is the superstore sample database. 
Which field should be added in which place to understand the user's question? Please give a JSON object without any explanation.
"""

# Ollama API URL
ollama_instance = Ollama(base_url="http://localhost:11434",
model="test10")  # Adjust if your endpoint differs

def chat_with_ollama(user_input, previous_context):
    """
    Function to handle chat with the Ollama model, updating context with user input.
    """
    # Update context with user input
    updated_context = f"{previous_context}\nUser: {user_input}"

    print(updated_context)
    
    # Prepare the data to send to Ollama
    data = {
        "input": updated_context,
        "parameters": {"max_tokens": 100}  # Adjust parameters as necessary
    }

    # Send POST request to Ollama API
    try:
        response = requests.post(ollama_instance, json=data)
        response.raise_for_status()  # Raise an error for bad responses

        # Get the response content from Ollama
        ollama_response = response.json()
        response_content = ollama_response.get("output", "No response content")
    
    except Exception as e:
        response_content = f"Error communicating with Ollama: {e}"

    # Update context with the model's response
    updated_context += f"\nOllama: {response_content}"
    
    # Print the Ollama response
    print("Ollama:", response_content)
    
    return updated_context

def main():
    # Start with initial context
    current_context = context
    
    # Start a chat loop
    while True:
        # Take user input
        user_input = input("You: ")
        
        # If user types 'exit', break the loop
        if user_input.lower() == 'exit':
            print("Exiting chat...")
            break
        
        # Update and persist the conversation context
        current_context = chat_with_ollama(user_input, current_context)

if __name__ == "__main__":
    main()
