import streamlit as st
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

# Prompt user to enter the database URL
database_url = st.text_input("Enter your database URL:", "")

# Check if a database URL is provided
if database_url:
    st.write("Database URL provided:", database_url)
    
    # Try connecting to the database using the provided URL
    try:
        # Create a database engine
        engine = create_engine(database_url)
        
        # Connect to the database
        with engine.connect() as connection:
            st.success("Connected to the database successfully!")

            # Use the inspector to get the table names
            inspector = inspect(engine)
            tables = inspector.get_table_names()

            # If tables are available, let the user select one
            if tables:
                selected_table = st.selectbox("Select a table to use:", tables)
                st.write(f"Selected table: {selected_table}")

                # Fetch the first 5 rows of the selected table
                # Use backticks for MySQL or remove them if not needed
                query = text(f'SELECT * FROM `{selected_table}` LIMIT 5;')
                result = connection.execute(query)

                # Convert result to a DataFrame and display
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                st.write(f"First 5 rows of {selected_table}:")
                st.write(df)

            else:
                st.warning("No tables found in the database.")
    
    except SQLAlchemyError as e:
        st.error(f"Failed to connect to the database: {str(e)}")
else:
    st.warning("Please enter a valid database URL.")
