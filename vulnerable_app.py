import os
import sqlite3

# Vulnerability 1: Hardcoded Secret Key
AWSSecretKey = "AKIAIOSFODNN7EXAMPLE"
DB_PASSWORD = "super_secret_password_123"

def get_user_data(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Vulnerability 2: SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchall()

def ping_server(ip_address):
    # Vulnerability 3: OS Command Injection
    os.system(f"ping -c 4 {ip_address}")

def calculate_expression(expr):
    # Vulnerability 4: Arbitrary Code Execution via eval()
    return eval(expr)