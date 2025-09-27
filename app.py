from flask import Flask, request
import bcrypt
import json
import os

app = Flask(__name__)

USER_DB = 'users.json'
if not os.path.exists(USER_DB):
    with open(USER_DB, 'w') as f:
        f.write("{}")

def load_users():
    with open(USER_DB, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, 'w') as f:
        json.dump(users, f)

@app.route('/')
def home():
    return '<h2>Welcome! Go to /register or /login</h2>'

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode()
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

        users = load_users()
        users[username] = {'password': hashed_pw.decode()}
        save_users(users)
        return 'User registered! Go to /login'
    
    return '''
        <form method="post">
        Username: <input name="username"><br>
        Password: <input name="password" type="password"><br>
        <input type="submit">
        </form>
    '''

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode()
        users = load_users()
        if username in users:
            stored_hash = users[username]['password'].encode()
            if bcrypt.checkpw(password, stored_hash):
                return f"Welcome {username}! Password verified."
        return "Invalid credentials"
    
    return '''
        <form method="post">
        Username: <input name="username"><br>
        Password: <input name="password" type="password"><br>
        <input type="submit">
        </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
