import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re

def load_data(file_path):
    """Load CSV data into a DataFrame."""
    df = pd.read_csv(file_path)
    return df

def analyze_data(df):
    """Analyze the DataFrame structure."""
    info = {
        'columns': df.columns.tolist(),
        'types': df.dtypes.to_dict(),
        'sample_rows': df.head().to_dict(orient='records')
    }
    return info

def preprocess_query(query):
    """Preprocess the natural language query."""
    query = query.lower()
    query = re.sub(r'[^\w\s]', '', query)
    return query

def query_llama(query, df_info, model, tokenizer):
    """Use LLaMA to parse the natural language query and identify filters."""
    df_columns = ', '.join(df_info['columns'])
    prompt = f"""
    You are given a DataFrame with the following columns: {df_columns}.
    Based on the natural language query, determine which columns and conditions should be used to filter the data.

    Query: "{query}"

    Provide the column names to be filtered and the conditions to apply. Output in JSON format.
    """
    
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs['input_ids'], max_length=150, num_return_sequences=1)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Parse result (assume result is in JSON format for simplicity)
    try:
        filters = eval(result)  # Use with caution; safer methods include parsing structured output
    except:
        print("Error parsing LLaMA response.")
        filters = {}

    return filters

def apply_filters(df, filters):
    """Apply filters to the DataFrame based on LLaMA's output."""
    filtered_df = df.copy()
    
    # Example of applying filters based on LLaMA response
    if 'columns' in filters:
        for col in filters['columns']:
            if col in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[col].notnull()]
    
    if 'conditions' in filters:
        for condition in filters['conditions']:
            col, operator, value = condition
            if col in filtered_df.columns:
                if operator == 'equals':
                    filtered_df = filtered_df[filtered_df[col] == value]
                elif operator == 'contains':
                    filtered_df = filtered_df[filtered_df[col].str.contains(value, case=False, na=False)]
    
    return filtered_df

def create_pivot_table(df):
    """Create and sort a pivot table from the DataFrame."""
    if 'company' in df.columns and 'quarter' in df.columns and 'value' in df.columns:
        pivot_table = pd.pivot_table(df, values='value', index='company', columns='quarter', aggfunc='sum', fill_value=0)
        sorted_pivot_table = pivot_table.sort_index(axis=1)  # Sort columns (quarters) in order
        return sorted_pivot_table
    else:
        print("Required columns for pivot table are missing.")
        return pd.DataFrame()  # Return an empty DataFrame if required columns are not present

def plot_pivot_table(pivot_table):
    """Plot the pivot table using matplotlib."""
    import matplotlib.pyplot as plt

    pivot_table.plot(kind='bar', figsize=(12, 8))
    plt.title('Revenue by Company and Quarter')
    plt.xlabel('Company')
    plt.ylabel('Revenue')
    plt.legend(title='Quarter')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main(file_path, query):
    # Load and analyze the data
    df = load_data(file_path)
    data_info = analyze_data(df)
    print("Data Structure Analysis:")
    print(data_info)
    
    # Load LLaMA model and tokenizer
    model_name = "meta-llama/llama-7b"  # Update with the correct model name if different
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # Preprocess and query LLaMA
    preprocessed_query = preprocess_query(query)
    filters = query_llama(preprocessed_query, data_info, model, tokenizer)
    
    # Apply filters and get the results
    filtered_df = apply_filters(df, filters)
    
    # Check filtered data
    print("\nFiltered Data:")
    print(filtered_df.head())
    
    # Create and display the pivot table
    pivot_table = create_pivot_table(filtered_df)
    print("\nPivot Table:")
    print(pivot_table)
    
    # Plot the pivot table
    plot_pivot_table(pivot_table)

# Example usage
if __name__ == "__main__":
    csv_file_path = '/Users/manavpanwar/Downloads/newdata.csv'
    user_query = 'Show me the revenue of 20 Microns Ltd. company from first quarter to last'
    main(csv_file_path, user_query)
