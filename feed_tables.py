import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les informations de connexion à la base de données
DB_HOST = "localhost"
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

# Dossier contenant les fichiers CSV
DATASET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Liste des fichiers CSV et leurs tables cibles
csv_files = {
    "symptoms.csv": "symptoms",
    "diseases.csv": "diseases",
    #"treatment_FR.csv": "treatment_FR",
}

def table_exists(conn, table_name):
    """ Vérifie si la table existe dans la base de données """
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')")
        return cursor.fetchone()[0]

def drop_table(conn, table_name):
    """ Supprime la table si elle existe """
    if table_exists(conn, table_name):
        with conn.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
        print(f"✅ Table '{table_name}' supprimée avec succès.")

def get_column_lengths(df):
    """ Retourne un dictionnaire avec la longueur maximale de chaque colonne """
    column_lengths = {}
    for column in df.columns:
        max_length = df[column].apply(lambda x: len(str(x))).max()
        column_lengths[column] = max_length
    return column_lengths

def create_table(conn, table_name, columns, column_lengths):
    """ Crée une table avec les colonnes spécifiées et tailles ajustées """
    column_definitions = ", ".join([f"{col} VARCHAR({column_lengths[col]})" for col in columns])
    create_table_query = f"""
    CREATE TABLE {table_name} (
        {column_definitions}
    );
    """
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
    print(f"✅ Table '{table_name}' créée avec succès.")

def insert_data_from_csv(csv_path, table_name, conn):
    """ Insère les données d'un fichier CSV dans une table PostgreSQL """
    df = pd.read_csv(csv_path)
    
    # Calculer la taille maximale des colonnes
    column_lengths = get_column_lengths(df)
    
    # Supprimer la table si elle existe déjà
    drop_table(conn, table_name)
    
    # Créer la table
    create_table(conn, table_name, df.columns, column_lengths)
    
    with conn.cursor() as cursor:
        # Générer la requête SQL d'insertion dynamique
        columns = ", ".join(df.columns)
        values_placeholder = ", ".join(["%s"] * len(df.columns))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholder})"
        
        # Insérer chaque ligne du DataFrame dans la base de données
        for row in df.itertuples(index=False, name=None):
            cursor.execute(query, row)

    print(f"✅ Données insérées dans '{table_name}' avec succès.")

conn = None  # Initialiser la variable de connexion pour éviter les erreurs de référence

try:
    # Connexion à la base de données
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True  # Valide automatiquement les transactions

    for csv_file, table_name in csv_files.items():
        file_path = os.path.join(DATASET_DIR, csv_file)
        
        if os.path.exists(file_path):  # Vérifier si le fichier existe
            insert_data_from_csv(file_path, table_name, conn)
        else:
            print(f"⚠️ Le fichier '{csv_file}' n'existe pas.")

    print("🎉 Importation des fichiers CSV terminée avec succès !")

except Exception as e:
    print(f"❌ Erreur : {e}")

finally:
    if conn:
        conn.close()
        print("🔌 Connexion à la base de données fermée.")
    else:
        print("❌ La connexion à la base de données n'a pas pu être établie.")
