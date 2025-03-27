import json
import os
import subprocess
from datetime import datetime

participants_path = "participants.json"
erreurs_path = "a_verifier_manuellement.txt"
photos_path = "photos/dossards_a_verifier"

# 📂 Charger les participants
with open(participants_path, "r") as f:
    participants = json.load(f)

# 📄 Lire les dossards à vérifier
with open(erreurs_path, "r") as f:
    lignes = [l.strip() for l in f.readlines() if l.strip()]

nouveau_contenu = []

for ligne in lignes:
    nom_fichier, dossard_detecte = ligne.split(",")

    chemin_photo = os.path.join(photos_path, nom_fichier)
    print(f"\n🖼️ Vérification de : {chemin_photo}")
    print(f"📸 Dossard détecté automatiquement : {dossard_detecte}")

    # 👉 Ouvre la photo avec le visualiseur par défaut (Linux/Mac/Windows)
    try:
        subprocess.run(["xdg-open", chemin_photo], check=False)  # Linux
    except FileNotFoundError:
        subprocess.run(["open", chemin_photo], check=False)  # macOS
        # Windows = os.startfile()

    # 🔤 Demander à l’utilisateur la correction
    correction = input("➡️  Numéro correct (laisser vide pour ignorer) : ").strip()

    if correction:
        if correction not in participants:
            # Ajouter nouveau coureur si non présent
            nom = input("👤 Nom du participant : ").strip()
            participants[correction] = {"nom": nom, "temps": []}

        # Ajouter le temps de passage actuel
        timestamp = datetime.now().isoformat()
        participants[correction]["temps"].append(timestamp)
        print(f"✅ Ajouté pour {correction} à {timestamp}")

        # Supprimer ou archiver l’image traitée
        os.remove(chemin_photo)
    else:
        nouveau_contenu.append(ligne)  # Laisse dans la liste à revoir plus tard

# 💾 Sauvegarder la liste mise à jour
with open(erreurs_path, "w") as f:
    for ligne in nouveau_contenu:
        f.write(ligne + "\n")

# 💾 Sauvegarder les participants
with open(participants_path, "w") as f:
    json.dump(participants, f, indent=2)

print("\n🎉 Vérification manuelle terminée.")
