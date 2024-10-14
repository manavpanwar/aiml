from langchain.llms import Ollama  # Ensure this is the correct import

# Create an instance of the Ollama model
ollama_instance = Ollama(base_url='http://122.176.146.28:11434', model="vizlab")

# Ask a question and print the response
try:
    response = ollama_instance("Why is the sky blue?")  # Use the instance to call the model
    print(response)
except Exception as e:
    print(f"An error occurred: {e}")
