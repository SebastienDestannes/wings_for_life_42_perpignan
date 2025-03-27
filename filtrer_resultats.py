import json
import datetime
import os
import shutil
from difflib import get_close_matches

# 📁 Fichiers
fichier_dossards = "resultats_batch.txt"
fichier_participants = "participants.json"
fichier_erreurs = "a_verifier_manuellement.txt"

# 📁 Dossiers
photos_source_dir = "photos/photos_brutes"
photos_erreurs_dir = "photos/dossards_a_verifier"

# 📂 Création du dossier erreurs s’il n’existe pas
os.makedirs(photos_erreurs_dir, exist_ok=True)

# 🧠 Chargement des dossards officiels
with open(fichier_participants, "r") as f:
    participants = json.load(f)

# 📄 Liste des lignes à analyser
with open(fichier_dossards, "r") as f:
    lignes = [l.strip() for l in f.readlines() if l.strip()]

# 🔁 Traitement des lignes
for ligne in lignes:
    nom_fichier, dossard_lu = ligne.split(",")
    dossard_lu = dossard_lu.strip()

    # 🕓 Extraction du timestamp depuis le nom du fichier
    try:
        date_str = nom_fichier.split("photo_")[1].split(".jpg")[0]
        date_str = date_str.replace(" (", "_").replace(")", "").replace("-", ":")
        horodatage = datetime.datetime.strptime(date_str, "%Y:%m:%d_%H:%M:%S")
    except Exception:
        horodatage = datetime.datetime.now()  # Fallback si erreur

    if dossard_lu in participants:
        # ✅ Correspondance exacte
        participants[dossard_lu]["temps"].append(horodatage.isoformat())
        print(f"✔️ {dossard_lu} détecté → temps enregistré")

    else:
        # 🔍 Tentative de correction avec correspondance approximative
        candidats_proches = get_close_matches(dossard_lu, participants.keys(), n=1, cutoff=0.7)
        if candidats_proches:
            dossard_corrige = candidats_proches[0]
            participants[dossard_corrige]["temps"].append(horodatage.isoformat())
            print(f"🔁 Correction : {dossard_lu} ≈ {dossard_corrige} → temps enregistré")
        else:
            # ❌ Dossard inconnu → à vérifier
            with open(fichier_erreurs, "a") as f:
                f.write(f"{nom_fichier},{dossard_lu}\n")

            # 📂 Copie de l'image source vers le dossier de vérification
            chemin_source = os.path.join(photos_source_dir, nom_fichier)
            chemin_destination = os.path.join(photos_erreurs_dir, nom_fichier)
            try:
                shutil.copy2(chemin_source, chemin_destination)
                print(f"❓ Dossard inconnu : {dossard_lu} → Copié dans {chemin_destination}")
            except FileNotFoundError:
                print(f"⚠️ Image introuvable pour copie : {chemin_source}")

# 💾 Mise à jour du fichier JSON
with open(fichier_participants, "w") as f:
    json.dump(participants, f, indent=2)

print("✅ Mise à jour des temps terminée.")
