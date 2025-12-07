# app.py
import streamlit as st
import os
from dotenv import load_dotenv
import sqlite3
from src.llm_logic import get_gemini_response, create_dynamic_prompt
from src.db_logic import get_db_schema, execute_sql_query
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found! Please set it in your .env file.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Streamlit App ---

st.set_page_config(page_title="Chat with your DB", page_icon="🛢️")
local_css("src/style.css") # Load the CSS

st.title("🤖 TEXT TO SQL LLM")
st.markdown("Upload your SQLite database, and I'll answer your questions about it!")

# 1. File Uploader & DB Connection
uploaded_file = st.file_uploader("Upload your SQLite database (.db) file", type=["db", "sqlite", "sqlite3"])

if uploaded_file:
    
    db_path = f"data/{uploaded_file.name}"
    with open(db_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        # Connect to the DB and get schema
        conn = sqlite3.connect(db_path)
        schema = get_db_schema(conn)
        
        st.session_state.conn = conn
        st.session_state.schema = schema
        
        st.success(f"Successfully connected to `{uploaded_file.name}`.")
        with st.expander("Show Database Schema"):
            st.text(schema)

    except Exception as e:
        st.error(f"An error occurred while connecting or reading the DB: {e}")
        if 'conn' in locals():
            conn.close()
        os.remove(db_path) 
        st.stop()

# 2. Chat Interface 
if 'conn' in st.session_state:
    st.header("Ask your question")
    question = st.text_input("e.g., 'How many students are in the Data Science class?'", key="input")
    submit = st.button("Generate Answer")

    if submit and question:
        with st.spinner("Generating SQL query and fetching results..."):
            try:
                
                prompt = create_dynamic_prompt(st.session_state.schema)
                
                sql_query = get_gemini_response(question, prompt)
                
                with st.expander("Generated SQL Query"):
                    st.code(sql_query, language="sql")
                
                
                data = execute_sql_query(sql_query, st.session_state.conn)
                
                
                st.subheader("Query Results:")
                if data:
                    
                    import pandas as pd
                    df = pd.DataFrame(data)
                    st.dataframe(df)
                else:
                    st.warning("The query returned no results.")
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a database file to get started.")