import mysql.connector
import pandas as pd
from langchain_groq import ChatGroq

# Initialize context and API key for GroqCloud
context = """
You are a pivot table expert. You need to organize data fields into rows, values, filters, and columns. Your database is the superstore sample database. 
Which field should be added in which place to unnderstand users question? Please give a JSON object without any explanation.
"""

# Initialize the GroqCloud model
llm = ChatGroq(
    temperature=0,
    api_key="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",
    model="mixtral-8x7b-32768",
)

def chat_with_groq(user_input, previous_context):
    """
    Function to handle chat with the GroqCloud model, updating context with user input.
    """
    # Update context with user input
    updated_context = f"{previous_context}\nUser: {user_input}"

    print(updated_context)
    
    # Generate response from GroqCloud
    response = llm.invoke(updated_context)
    
    # Update context with the model's response
    updated_context += f"\nGroq: {response.content}"
    
    # Print the Groq response
    print("Groq:", response.content)
    
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
        current_context = chat_with_groq(user_input, current_context)

if __name__ == "__main__":
    main()