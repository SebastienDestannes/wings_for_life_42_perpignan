import datetime
import os
import shutil
import psycopg2
from dotenv import load_dotenv
from difflib import get_close_matches

# 🔐 Charger .env
load_dotenv()
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}
CHECKPOINT_ID = int(os.getenv("CHECKPOINT_ID", 1))

# 📁 Fichiers
fichier_dossards = "resultats_batch.txt"
fichier_erreurs = "a_verifier_manuellement.txt"
photos_source_dir = "photos/photos_brutes"
photos_erreurs_dir = "photos/dossards_a_verifier"
os.makedirs(photos_erreurs_dir, exist_ok=True)

# 📡 Connexion à la BDD
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# 🔍 Charger tous les id_runner connus
cur.execute("SELECT id_runner FROM participant_data")
connus = {str(row[0]) for row in cur.fetchall()}

# 📄 Lire le fichier des résultats
with open(fichier_dossards, "r") as f:
    lignes = [l.strip() for l in f.readlines() if l.strip()]

# 🔁 Traitement
for ligne in lignes:
    nom_fichier, dossard_lu = ligne.split(",")
    dossard_lu = dossard_lu.strip()

    # 📅 Timestamp depuis le nom de fichier
    try:
        date_str = nom_fichier.split("photo_")[1].split(".jpg")[0]
        horodatage = datetime.datetime.strptime(date_str, "%Y%m%d_%H%M%S")
    except Exception:
        horodatage = datetime.datetime.now()

    image_id = nom_fichier.rsplit(".", 1)[0]

    if dossard_lu in connus:
        id_runner = int(dossard_lu)

    else:
        proches = get_close_matches(dossard_lu, connus, n=1, cutoff=0.7)
        if proches:
            id_runner = int(proches[0])
            print(f"🔁 Correction automatique : {dossard_lu} → {id_runner}")
        else:
            # ❌ Inconnu → vérification manuelle
            with open(fichier_erreurs, "a") as f:
                f.write(f"{nom_fichier},{dossard_lu}\n")
            try:
                shutil.copy2(os.path.join(photos_source_dir, nom_fichier),
                             os.path.join(photos_erreurs_dir, nom_fichier))
            except FileNotFoundError:
                pass
            continue

    # ✅ Insertion en base
    cur.execute("""
        INSERT INTO raw_data_income_ia (
            checkpoint_id, is_starting_checkpoint,
            income_id_runner, image_id, last_time_saw_at,
            is_treated, is_noise_data
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        CHECKPOINT_ID,
        False,
        id_runner,
        image_id,
        horodatage,
        False,
        False
    ))
    print(f"✔️ Passage de {id_runner} inséré à {horodatage.isoformat()}")

# 💾 Finalisation
conn.commit()
cur.close()
conn.close()
print("✅ Tous les dossards connus ont été traités.")
