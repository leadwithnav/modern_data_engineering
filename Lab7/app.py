from flask import Flask, request
import psycopg2
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <h2>User Form</h2>
        <form method="POST" action="/submit">
            <label>Username:</label>
            <input type="text" name="username" required><br><br>
            <label>Age:</label>
            <input type="number" name="age" required><br><br>
            <input type="submit" value="Submit">
        </form>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    age = request.form.get('age')

    try:
        with open("/mnt/secrets/DB_USER", "r") as ufile:
            db_user = ufile.read().strip()
        with open("/mnt/secrets/DB_PASSWORD", "r") as pfile:
            db_password = pfile.read().strip()

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "postgres-service"),
            database=os.getenv("DB_NAME", "flaskdb"),
            user=db_user,
            password=db_password
        )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                age INTEGER NOT NULL
            );
        """)
        cur.execute("INSERT INTO users (username, age) VALUES (%s, %s);", (username, age))
        conn.commit()
        cur.close()
        conn.close()
        return f"<h3>Thank you, {username}! Your age {age} has been recorded.</h3>"
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
