from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from config import DATABASE_CONFIG

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (for frontend)

# Connect to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the DeepWine API!"})

# Endpoint to fetch all wines
@app.route('/wines', methods=['GET'])
def get_wines():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, grape_variety, region, alcohol_content, flavor_profile, food_pairings FROM wines;")
    wines = cursor.fetchall()
    conn.close()

    wine_list = []
    for wine in wines:
        wine_list.append({
            "id": wine[0],
            "name": wine[1],
            "grape_variety": wine[2],
            "region": wine[3],
            "alcohol_content": wine[4],
            "flavor_profile": wine[5],
            "food_pairings": wine[6]
        })

    return jsonify(wine_list)

# Endpoint to recommend a wine based on flavor profile
@app.route('/recommend', methods=['POST'])
def recommend_wine():
    data = request.json
    flavor = data.get("flavor_profile", "")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, grape_variety, region FROM wines WHERE flavor_profile ILIKE %s LIMIT 5", (f"%{flavor}%",))
    wines = cursor.fetchall()
    conn.close()

    recommendations = [{"name": wine[0], "grape_variety": wine[1], "region": wine[2]} for wine in wines]

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)

