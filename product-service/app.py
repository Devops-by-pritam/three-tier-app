from flask import Flask
import psycopg2

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host="DB_HOST",
        user="DB_USER",
        password="DB_PASS",
        dbname="products_db"
    )

@app.route("/products")
def get_products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM products;")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"products": [r[0] for r in results]}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
