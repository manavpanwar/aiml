# %%
import warnings
from langchain.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

# Suppress specific deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Initialize Ollama instance with your model server details
ollama_instance = Ollama(base_url="http://122.176.146.28:11434", model="test14")

# %%
# Prompt template for generating responses
template = """You are a helpful assistant. You are chatting with a user.
The conversation history is:
{history}

User: {input}
Assistant:"""

prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=template,
)

# %%
# Langchain memory to store the conversation context
memory = ConversationBufferMemory()

# Define the ConversationChain with Ollama LLM
conversation_chain = ConversationChain(
    llm=ollama_instance,
    prompt=prompt,
    memory=memory,
)

# %%
# Start chatting
print("Chatbot: Hi! How can I assist you today?")
while True:
    # Get user input
    user_input = input("User: ")
    
    # Exit if the user types 'exit'
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    # Generate a response using Langchain's conversation chain
    response = conversation_chain.predict(input=user_input)

    # Print the assistant's response
    print(f"Chatbot: {response}")

# %%
