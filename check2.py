import mysql.connector
import pandas as pd
from langchain_groq import ChatGroq

# Step 2: Write a query to fetch the data you're interested in
query = """
    SELECT company, sector, value, quarter
    FROM your_table
    WHERE quarter >= '2024-04-01' AND quarter <= '2024-06-30'
"""

context = "You are a pivot table expert, you need to put data fields into rows, values, filters, columns, your database is the superstore sample database. what field should be added in which place to understand state wise sales trend for South, please give a json object without any explanation"
question = "Are you familiar with superstore database which is used for BI testing"

# Step 4: Invoke GroqCloud to process the question
llm = ChatGroq(
    temperature=0,
    api_key="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",
    model="mixtral-8x7b-32768",
)

response = llm.invoke(context)
parsed_question = response.content
print("Parsed Question:", parsed_question)


