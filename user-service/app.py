from flask import Flask
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="DB_HOST",
        user="DB_USER",
        password="DB_PASS",
        database="users_db"
    )

@app.route("/users")
def get_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users;")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"users": [r[0] for r in results]}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
