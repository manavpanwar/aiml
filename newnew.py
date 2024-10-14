import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Step 1: Read the CSV file
csv_file_path = '/Users/manavpanwar/Downloads/Complete.csv'  # Change to your CSV file path
df = pd.read_csv(csv_file_path)

# Step 2: Extract distinct values from a specific column (e.g., 'company')
distinct_values = df['company'].unique()

# Convert to a list for easier searching
distinct_values_list = distinct_values.tolist()

# Step 3: Set up LLaMA model
model_name = "meta-llama/Llama-2-7b-chat-hf"  # Change to the appropriate model path
token = "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"  # Replace with your actual access token
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=token)

def search_values(query):
    # Step 4: Encode and process the query
    inputs = tokenizer.encode(query, return_tensors='pt')
    outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Assuming the response is a distinct value we want to search for
    return response.strip()  # Clean up the response

# Example natural language query
query = "What companies are in the data?"
searched_value = search_values(query)

# Step 5: Find rows corresponding to the searched value
filtered_data = df[df['company'].str.contains(searched_value, case=False, na=False)]

# Step 6: Create a pivot table
pivot_table = pd.pivot_table(filtered_data, index='company', columns='parameter', values='value', aggfunc='mean')

# Display the results
print(pivot_table)
