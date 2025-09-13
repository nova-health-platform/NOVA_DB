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


def get_connection():
    """Créer une nouvelle connexion PostgreSQL"""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# --- SYMPTOMS ---
def get_symptoms():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT symptom FROM symptoms")
    symptoms = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in symptoms]

@app.route('/symptoms', methods=['GET'])
def get_symptoms_api():
    try:
        return jsonify(get_symptoms())
    except Exception as e:
        print(f"Erreur : {str(e)}")
        return jsonify({"error": f"Erreur de récupération des symptômes : {str(e)}"}), 500


# --- SYNONYMS ---
def get_all_synonyms():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT symptom, synonyms FROM symptoms_synonyms_en")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"symptom": r[0], "synonyms": r[1]} for r in records]

def get_synonyms_by_symptom(symptom):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT symptom, synonyms FROM symptoms_synonyms_en WHERE symptom = %s", (symptom,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    if record:
        return {"symptom": record[0], "synonyms": record[1]}
    return None

@app.route('/symptoms/synonyms', methods=['GET'])
def get_all_synonyms_api():
    try:
        return jsonify(get_all_synonyms())
    except Exception as e:
        print(f"Erreur : {str(e)}")
        return jsonify({"error": f"Erreur de récupération des synonymes : {str(e)}"}), 500

@app.route('/symptoms/<string:symptom>/synonyms', methods=['GET'])
def get_synonyms_api(symptom):
    try:
        record = get_synonyms_by_symptom(symptom)
        if not record:
            return jsonify({"error": "Symptom not found"}), 404
        return jsonify(record)
    except Exception as e:
        print(f"Erreur : {str(e)}")
        return jsonify({"error": f"Erreur de récupération des synonymes : {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
