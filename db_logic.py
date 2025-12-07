# src/db_logic.py

import sqlite3

def get_db_schema(conn):
    """
    Fetches the schema of the SQLite database.
    """
    schema_str = ""
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        schema_str += f"Table '{table_name}':\n"
        
        # Get column info for each table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        for col in columns:
            # col[1] is name, col[2] is type
            schema_str += f"  - {col[1]} ({col[2]})\n"
        schema_str += "\n"
        
    return schema_str

def execute_sql_query(sql, conn):
    """
    Executes the given SQL query on the database.
    """
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    return rows