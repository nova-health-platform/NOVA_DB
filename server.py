from flask import Flask, jsonify
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration de la connexion PostgreSQL
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

# Fonction pour se connecter à PostgreSQL et récupérer les symptômes
def get_symptoms():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    cursor.execute("SELECT symptom FROM symptoms") 
    symptoms = cursor.fetchall()

    cursor.close()
    conn.close()

    return [row[0] for row in symptoms]


@app.route('/symptoms', methods=['GET'])
def get_symptoms_api():
    try:
        symptoms = get_symptoms()
        return jsonify(symptoms)
    except Exception as e:
        print(f"Erreur : {str(e)}")  # Log l'erreur
        return jsonify({"error": f"Erreur de récupération des symptômes : {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
