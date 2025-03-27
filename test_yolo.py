from ultralytics import YOLO
import cv2
import time
import pytesseract
import re

# 🔧 Fonction pour tester plusieurs angles de rotation et trouver celui donnant le meilleur OCR
def deskew_best_rotation(image, max_angle=15):
    """
    Essaye plusieurs rotations de -max_angle à +max_angle degrés
    pour corriger une inclinaison du texte (deskew).
    Retourne l'image redressée et le meilleur numéro détecté (4 à 6 chiffres).
    """
    best_image = image
    best_text = ""
    config = '--psm 6 -c tessedit_char_whitelist=0123456789'

    for angle in range(-max_angle, max_angle + 1, 2):  # de -15° à +15°, par pas de 2
        (h, w) = image.shape[:2]
        M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h),
                                 flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        # Préparation pour OCR
        gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Lecture OCR
        text = pytesseract.image_to_string(thresh, config=config).strip()

        # On garde le plus long groupe de 4 à 6 chiffres
        matches = re.findall(r"\d{4,6}", text)
        if matches:
            candidate = max(matches, key=len)
            if len(candidate) > len(best_text):
                best_text = candidate
                best_image = rotated

    return best_image, best_text


# 📦 Chargement du modèle YOLOv8 entraîné pour détecter les dossards
model = YOLO("runs/detect/train/weights/best.pt")

# 📷 Chargement de l’image
img = cv2.imread("coureurs.jpg")
assert img is not None, "Image non trouvée"

# ⏱️ Exécution de la détection
start = time.time()
results = model(img)
duration = time.time() - start
detections = results[0].boxes

print(f"⏱️ Prédiction YOLO faite en {duration:.2f} secondes")

# ✅ Affichage des résultats de détection
if detections is None or len(detections) == 0:
    print("❌ Aucun dossard détecté")
else:
    print(f"✅ {len(detections)} dossard(s) détecté(s) :")

    for box, cls_id, conf in zip(detections.xyxy, detections.cls, detections.conf):
        if conf < 0.1:  # seuil de confiance minimal
            continue
        x1, y1, x2, y2 = map(int, box)
        label = model.names[int(cls_id)]
        print(f"  ➤ '{label}' à ({x1}, {y1}) avec confiance {conf:.2f}")
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

# 💾 Sauvegarde de l’image avec les boîtes de détection
cv2.imwrite("resultats_detection.jpg", img)
print("✅ Image enregistrée : resultats_detection.jpg")

# 📜 Liste pour stocker les numéros de dossards détectés
bib_numbers = []

# 🔍 OCR sur chaque dossard détecté
for i, (box, conf) in enumerate(zip(detections.xyxy, detections.conf)):
    if conf < 0.3:
        continue

    # 🔲 Extraction de la zone du dossard avec petit padding
    x1, y1, x2, y2 = map(int, box)
    padding = 5
    x1p = max(x1 + padding, 0)
    x2p = min(x2 - padding, img.shape[1])
    y1p = max(y1 + padding, 0)
    y2p = min(y2 - padding, img.shape[0])
    roi = img[y1p:y2p, x1p:x2p]

    # 💾 Sauvegarde du crop original
    cv2.imwrite(f"dossard_{i}.jpg", roi)

    # 🌀 Correction d’inclinaison + OCR optimisé
    deskewed, best_text = deskew_best_rotation(roi, max_angle=15)

    # 💾 Sauvegarde du crop redressé
    cv2.imwrite(f"dossard_{i}_deskewed.jpg", deskewed)

    # ✅ Résultat OCR
    if best_text:
        bib_numbers.append(best_text)
        print(f"📖 OCR optimisé dans dossard_{i} : {best_text}")
    else:
        print(f"📖 Aucun numéro valide trouvé dans dossard_{i}")

# 💾 Sauvegarde des numéros détectés dans un fichier texte
with open("resultats_bib.txt", "w") as f:
    for num in bib_numbers:
        f.write(num + "\n")

print("✅ Résultats OCR enregistrés dans resultats_bib.txt")
