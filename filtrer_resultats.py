import json
import datetime
from difflib import get_close_matches

# 📁 Fichiers
fichier_dossards = "resultats_batch.txt"
fichier_participants = "participants.json"
fichier_erreurs = "a_verifier_manuellement.txt"

# 🧠 Chargement des dossards officiels
with open(fichier_participants, "r") as f:
    participants = json.load(f)

# 📄 Liste des lignes à analyser
with open(fichier_dossards, "r") as f:
    lignes = [l.strip() for l in f.readlines() if l.strip()]

# 📦 Résultat temporaire pour mise à jour des temps
dossards_vus = {}

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
            print(f"❓ Dossard inconnu : {dossard_lu} (image à vérifier : {nom_fichier})")

# 💾 Mise à jour du fichier JSON
with open(fichier_participants, "w") as f:
    json.dump(participants, f, indent=2)

print("✅ Mise à jour des temps terminée.")
