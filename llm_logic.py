# src/llm_logic.py

import google.generativeai as genai
import re

def get_gemini_response(question, prompt):
    """
    Gets the SQL query from the Gemini model.
    """
    model = genai.GenerativeModel('gemini-2.5-flash') 
    response = model.generate_content([prompt, question])
    
    # Clean up the response
    result = response.text
    
    match = re.search(r"```(sql)?\n(.*)```", result, re.DOTALL | re.IGNORECASE)
    if match:
        sql_query = match.group(2).strip()
    else:
        
        sql_query = result.strip().replace("'''", "").replace("sql", "", 1)
        
    return sql_query

def create_dynamic_prompt(schema):
    """
    Creates a dynamic prompt for the LLM based on the database schema.
    """
    prompt = f"""
    You are an expert in converting English questions to SQL queries!
    The SQL database has the following schema:

    {schema}

    Your job is to write a SQL query based on the user's question.
    Only output the SQL query, with no other text, explanations, or markdown.
    Do not use triple backticks (```) or the word 'sql' in your output.

    For example:
    Question: "How many entries of records are present?"
    SQL Query: SELECT COUNT(*) FROM STUDENT;

    Question: "Tell me all the students studying in data science class?"
    SQL Query: SELECT * FROM STUDENT WHERE CLASS="Data Science";
    """
    return prompt