from flask import Flask, request
import psycopg2

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
        conn = psycopg2.connect(
            host="postgres-service",
            database="flaskdb",
            user="flaskuser",
            password="flaskpass"
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