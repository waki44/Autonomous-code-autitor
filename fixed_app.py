import os
import sqlite3

# Vulnerability 1: Hardcoded Secret Key
AWSSecretKey = "AKIAIOSFODNN7EXAMPLE"
DB_PASSWORD = os.environ.get("DB_PASSWORD")

def get_user_data(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Vulnerability 2: SQL Injection
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return cursor.fetchall()

def ping_server(ip_address):
    # Vulnerability 3: OS Command Injection
    import subprocess
    subprocess.run(["ping", "-c", "4", ip_address])

def calculate_expression(expr):
    # Vulnerability 4: Arbitrary Code Execution via eval()
    import ast
    return ast.literal_eval(expr)