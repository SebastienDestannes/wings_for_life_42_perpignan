import os
import time
import cv2
import pytesseract
import re
from ultralytics import YOLO

# 📁 Dossier contenant les images à analyser (rempli par le script de capture webcam)
input_dir = "photos/photos_brutes"

# 📝 Fichier où seront enregistrés les résultats (numéros de dossards détectés)
output_txt = "resultats_batch.txt"

# 🧠 On garde en mémoire les images déjà traitées pour ne pas les analyser deux fois
déjà_vues = set()

# 📦 Pour stocker les résultats en mémoire (optionnel ici, juste pour log)
bib_numbers = {}

# 🔍 Chargement du modèle YOLO entraîné (à adapter si le chemin change)
model = YOLO("runs/detect/train/weights/best.pt")

# 🧠 Fonction OCR avec correction d'inclinaison
def deskew_best_rotation(image, max_angle=15):
    """
    Tente plusieurs petites rotations de l'image (-15 à +15 degrés),
    et garde le texte OCR le plus long (4 à 6 chiffres).
    Cela aide à corriger les dossards mal alignés.
    """
    best_text = ""
    config = '--psm 6 -c tessedit_char_whitelist=0123456789'

    for angle in range(-max_angle, max_angle + 1, 2):
        h, w = image.shape[:2]
        M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h),
                                 flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        # Conversion en niveau de gris + seuillage binaire pour OCR
        gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Lancement de l’OCR
        text = pytesseract.image_to_string(thresh, config=config).strip()

        # On ne garde que les séquences de chiffres de 4 à 6 chiffres
        matches = re.findall(r"\d{4,6}", text)
        if matches:
            candidate = max(matches, key=len)
            if len(candidate) > len(best_text):
                best_text = candidate  # On garde le meilleur résultat

    return best_text


print("📂 Surveillance du dossier en cours... CTRL+C pour arrêter.")

try:
    while True:
        # 🧾 Liste des fichiers .jpg présents dans le dossier
        images = sorted(f for f in os.listdir(input_dir) if f.lower().endswith(".jpg"))

        # 🎯 On filtre pour ne traiter que les nouvelles images
        new_images = [f for f in images if f not in déjà_vues]

        for img_name in new_images:
            img_path = os.path.join(input_dir, img_name)
            img = cv2.imread(img_path)

            if img is None:
                print(f"⚠️ Image illisible : {img_name}")
                continue

            # 🔍 YOLO détecte les dossards
            results = model(img)
            detections = results[0].boxes
            detected_bibs = []

            # 📦 Pour chaque dossard détecté
            for box, conf in zip(detections.xyxy, detections.conf):
                if conf < 0.3:
                    continue  # On ignore les détections peu fiables

                x1, y1, x2, y2 = map(int, box)

                # ✂️ On ajoute un petit padding pour éviter de couper le dossard
                padding = 5
                x1p = max(x1 + padding, 0)
                x2p = min(x2 - padding, img.shape[1])
                y1p = max(y1 + padding, 0)
                y2p = min(y2 - padding, img.shape[0])
                roi = img[y1p:y2p, x1p:x2p]

                # 🌀 OCR avec redressement automatique
                best_text = deskew_best_rotation(roi)

                if best_text:
                    detected_bibs.append(best_text)
                    print(f"📖 {img_name} ➤ {best_text}")

            # 📝 Enregistrement dans un fichier texte
            if detected_bibs:
                bib_numbers[img_name] = detected_bibs

                with open(output_txt, "a") as f:
                    for number in detected_bibs:
                        f.write(f"{img_name},{number}\n")

            # ✅ On marque cette image comme déjà traitée
            déjà_vues.add(img_name)

        # 💤 Pause avant le prochain scan
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n🛑 Surveillance arrêtée manuellement.")
