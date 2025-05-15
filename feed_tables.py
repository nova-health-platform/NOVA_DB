import pandas as pd
import psycopg2
import os
import re
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# 🔌 Connexion BDD
DB_HOST = "localhost"
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

# 📁 Répertoire des CSV
DATASET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# 📄 Fichiers CSV à importer
csv_files = {
    "symptoms.csv": "symptoms",
    "diseases.csv": "diseases",
    # "treatment_FR.csv": "treatment_FR",
}

def table_exists(conn, table_name):
    with conn.cursor() as cursor:
        cursor.execute(f"""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_name = %s
            )
        """, (table_name,))
        return cursor.fetchone()[0]

def drop_table(conn, table_name):
    if table_exists(conn, table_name):
        with conn.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
        print(f"✅ Table '{table_name}' supprimée avec succès.")

def get_column_lengths(df):
    return {col: df[col].apply(lambda x: len(str(x))).max() for col in df.columns}

def create_table(conn, table_name, columns, column_lengths):
    column_definitions = ", ".join([f"{col} VARCHAR({column_lengths[col]})" for col in columns])
    create_query = f"CREATE TABLE {table_name} ({column_definitions});"
    with conn.cursor() as cursor:
        cursor.execute(create_query)
    print(f"✅ Table '{table_name}' créée avec succès.")

def insert_data_from_csv(csv_path, table_name, conn):
    df = pd.read_csv(csv_path)
    column_lengths = get_column_lengths(df)
    drop_table(conn, table_name)
    create_table(conn, table_name, df.columns, column_lengths)
    
    with conn.cursor() as cursor:
        columns = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        for row in df.itertuples(index=False, name=None):
            cursor.execute(insert_query, row)

    print(f"✅ Données insérées dans '{table_name}' avec succès.")

# 🧽 Nettoyage de la colonne pain_location
def normalize_pain_location_string(raw_str):
    if not raw_str:
        return ""
    cleaned = (
        raw_str.lower()
        .replace(".", "")
        .replace(" ,", ",")
        .replace(", ", ",")
        .replace(" ", "_")
        .strip()
    )
    parts = list(dict.fromkeys(cleaned.split(",")))  # Supprimer doublons
    return ",".join(parts)

def clean_pain_location_column(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT disease_id, pain_location FROM diseases")
        rows = cursor.fetchall()
        updated = 0

        for disease_id, raw_value in rows:
            cleaned = normalize_pain_location_string(raw_value)
            if raw_value and raw_value.strip() != cleaned:
                cursor.execute(
                    "UPDATE diseases SET pain_location = %s WHERE disease_id = %s",
                    (cleaned, disease_id)
                )
                updated += 1

        print(f"🧼 {updated} lignes mises à jour dans la colonne 'pain_location'.")

# 🔁 Script principal
conn = None
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True

    for csv_file, table_name in csv_files.items():
        file_path = os.path.join(DATASET_DIR, csv_file)
        if os.path.exists(file_path):
            insert_data_from_csv(file_path, table_name, conn)
        else:
            print(f"⚠️ Le fichier '{csv_file}' est introuvable.")

    # Nettoyage après import
    clean_pain_location_column(conn)

    print("🎉 Importation et nettoyage terminés avec succès.")

except Exception as e:
    print(f"❌ Erreur : {e}")

finally:
    if conn:
        conn.close()
        print("🔌 Connexion fermée.")
