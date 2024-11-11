import csv
import sqlite3
from datetime import datetime

conn = sqlite3.connect('../bd/data.bd')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS mineraux')
cursor.execute('''
CREATE TABLE mineraux (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nom TEXT,
    Commentaires TEXT,
    Provenance TEXT,
    Date_acquisition DATE,
    Prix_achat REAL,
    cm_g TEXT,
    autres_infos TEXT,
    Boite TEXT
)
''')


def convert_date_to_sql_date(date):
    if date:
        try:
            return datetime.strptime(date, '%d/%m/%Y').date().isoformat()
        except ValueError:
            print(f"Erreur de format de date pour {date}")
            return None
    return None


def parse_price(price_str):
    try:
        return float(price_str.replace('€', '').replace(',', '.').strip())
    except ValueError:
        print(f"Erreur de format de prix pour {price_str}")
        return None


with open('csvSource.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    conn.execute('BEGIN TRANSACTION')

    try:
        for row in reader:
            # Préparation des données pour l'insertion
            nom = row[0].strip() if row[0] else None
            commentaires = row[1].strip() if row[1] else None
            provenance = row[2].strip() if row[2] else None
            date_acquisition = convert_date_to_sql_date(row[3].strip()) if row[3] else None
            prix_achat = parse_price(row[4].strip()) if row[4] else None
            cm_g = row[5].strip() if row[5] else None
            autres_infos = row[6].strip() if row[6] else None
            boite = row[7].strip() if row[7] else None

            cursor.execute('''
                INSERT INTO mineraux (Nom, Commentaires, Provenance, Date_acquisition, Prix_achat, cm_g, autres_infos, Boite)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (nom, commentaires, provenance, date_acquisition, prix_achat, cm_g, autres_infos, boite))

        conn.commit()
        print("Données insérées avec succès dans la base de données.")
    except Exception as e:
        conn.rollback()
        print(f"Une erreur est survenue lors de l'insertion : {e}")

cursor.execute("SELECT * FROM mineraux")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
