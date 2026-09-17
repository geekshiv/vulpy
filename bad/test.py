import os
import subprocess
import pickle
import hashlib
import random
import requests
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# 1. Hardcoded Secret / API Key
API_KEY = "sk_live_1234567890abcdefghijklmnopqrstuvwxyz"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # 2. SQL Injection via string formatting
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password)
    cursor.execute(query) 
    
    # 3. Weak Cryptography (MD5 used for password hashing)
    hashed_pw = hashlib.md5(password.encode()).hexdigest()
    
    return "Attempted login"

@app.route('/ping', methods=['GET'])
def ping():
    target = request.args.get('host')
    
    # 4. Command Injection via shell=True
    result = subprocess.run(f"ping -c 1 {target}", shell=True, capture_output=True)
    return result.stdout

@app.route('/read', methods=['GET'])
def read_file():
    filename = request.args.get('filename')
    
    # 5. Path Traversal via untrusted file open
    with open(filename, 'r') as f:
        return f.read()

@app.route('/load', methods=['POST'])
def load_data():
    raw_data = request.data
    
    # 6. Insecure Deserialization using pickle
    data = pickle.loads(raw_data)
    return str(data)

@app.route('/calc', methods=['GET'])
def calculate():
    expr = request.args.get('expr')
    
    # 7. Unsafe Use of eval()
    return str(eval(expr))

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name')
    
    # 8. Server-Side Template Injection (SSTI) / XSS
    return render_template_string(f"Hello {name}")

@app.route('/external', methods=['GET'])
def fetch_external_data():
    # 9. Disabled SSL Verification in Requests
    response = requests.get("https://api.example.com/data", verify=False)
    return response.text

@app.route('/token', methods=['GET'])
def generate_token():
    # 10. Insecure Randomness (using standard random for potential security token)
    token = str(random.randint(100000, 999999))
    return token

if __name__ == '__main__':
    app.run(debug=True)
