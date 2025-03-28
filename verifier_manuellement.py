import json
import os
import subprocess
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

# 📥 Charger la config depuis .env
load_dotenv()
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}
CHECKPOINT_ID = int(os.getenv("CHECKPOINT_ID", 1))

# 📁 Chemins
erreurs_path = "a_verifier_manuellement.txt"
photos_path = "photos/dossards_a_verifier"

# 📂 Lire les lignes à traiter
with open(erreurs_path, "r") as f:
    lignes = [l.strip() for l in f.readlines() if l.strip()]

nouveau_contenu = []

# 🔌 Connexion à la base
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

for ligne in lignes:
    nom_fichier, dossard_detecte = ligne.split(",")

    chemin_photo = os.path.join(photos_path, nom_fichier)
    print(f"\n🖼️ Vérification de : {chemin_photo}")
    print(f"📸 Dossard détecté automatiquement : {dossard_detecte}")

    # 📷 Ouvrir l'image
    try:
        subprocess.run(["xdg-open", chemin_photo], check=False)  # Linux
    except FileNotFoundError:
        try:
            subprocess.run(["open", chemin_photo], check=False)  # macOS
        except FileNotFoundError:
            os.startfile(chemin_photo)  # Windows

    # 🧠 Demander à l’utilisateur
    correction = input("➡️  Numéro correct (laisser vide pour ignorer) : ").strip()

    if correction:
        id_runner = int(correction)

        # 💾 Vérifier si le coureur existe déjà
        cur.execute("SELECT 1 FROM participant_data WHERE id_runner = %s", (id_runner,))
        if cur.fetchone() is None:
            pseudo = input("👤 Nom ou pseudo du participant : ").strip()
            cur.execute(
                "INSERT INTO participant_data (id_runner, pseudo) VALUES (%s, %s)",
                (id_runner, pseudo)
            )
            print(f"✅ Ajouté dans participant_data : {id_runner} ({pseudo})")

        # 🕓 Créer l’horodatage et l’image_id
        timestamp = datetime.now()
        image_id = nom_fichier.rsplit(".", 1)[0]

        # ✅ Ajouter le passage dans raw_data_income_ia
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
            timestamp,
            True,
            False
        ))
        print(f"📥 Passage enregistré pour {id_runner} à {timestamp.isoformat()}")

        # 🧹 Nettoyage de l’image
        try:
            os.remove(chemin_photo)
        except FileNotFoundError:
            pass

    else:
        # 💤 Reporter la ligne pour plus tard
        nouveau_contenu.append(ligne)

# 💾 Mise à jour du fichier de lignes non traitées
with open(erreurs_path, "w") as f:
    for ligne in nouveau_contenu:
        f.write(ligne + "\n")

# 🔚 Sauvegarder et fermer
conn.commit()
cur.close()
conn.close()

print("\n🎉 Vérification terminée.")
