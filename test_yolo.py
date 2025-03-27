from ultralytics import YOLO
import cv2
import time
import pytesseract
import re


# 🔧 Fonction pour redresser une image inclinée (deskew)
def deskew_fixed(image, max_angle=15):
    """
    Effectue une correction légère d'inclinaison (rotation) jusqu'à max_angle degrés.
    On teste plusieurs angles et on garde celui où l'image est la plus 'dense' en texte OCR.
    """
    best_image = image
    best_text_len = 0
    config = '--psm 6 -c tessedit_char_whitelist=0123456789'

    for angle in range(-max_angle, max_angle + 1, 3):  # -15 à +15 degrés, par pas de 3
        (h, w) = image.shape[:2]
        M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h),
                                 flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(thresh, config=config)

        if len(text.strip()) > best_text_len:
            best_text_len = len(text.strip())
            best_image = rotated

    return best_image

def deskew_best_rotation(image, max_angle=15):
    """
    Teste plusieurs rotations entre -max_angle et +max_angle degrés
    et garde celle donnant le meilleur groupe de chiffres OCR.
    """
    best_image = image
    best_text = ""
    config = '--psm 6 -c tessedit_char_whitelist=0123456789'

    for angle in range(-max_angle, max_angle + 1, 2):  # -15 à +15 degrés, pas de 2
        (h, w) = image.shape[:2]
        M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h),
                                 flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(thresh, config=config).strip()

        matches = re.findall(r"\d{4,6}", text)
        if matches:
            candidate = max(matches, key=len)
            if len(candidate) > len(best_text):
                best_text = candidate
                best_image = rotated

    return best_image, best_text



# 📦 Charge ton modèle entraîné
model = YOLO("runs/detect/train/weights/best.pt")

# 📷 Charge l'image
img = cv2.imread("coureurs.jpg")
assert img is not None, "Image non trouvée"

# ⏱️ Prédiction YOLO
start = time.time()
results = model(img)
duration = time.time() - start
detections = results[0].boxes

print(f"⏱️ Prédiction YOLO faite en {duration:.2f} secondes")

if detections is None or len(detections) == 0:
    print("❌ Aucun caractère détecté")
else:
    print(f"✅ {len(detections)} caractères détectés :")

    # 🔲 Dessin des boîtes sur l’image
    for box, cls_id, conf in zip(detections.xyxy, detections.cls, detections.conf):
        if conf < 0.1:
            continue
        x1, y1, x2, y2 = map(int, box)
        char = model.names[int(cls_id)]
        print(f"  ➤ '{char}' à ({x1}, {y1}) avec confiance {conf:.2f}")
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, char, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

# 💾 Sauvegarde de l’image annotée
output_path = "resultats_detection.jpg"
cv2.imwrite(output_path, img)
print(f"✅ Image enregistrée : {output_path}")

bib_numbers = []


# 🔍 OCR sur chaque dossard détecté
for i, (box, conf) in enumerate(zip(detections.xyxy, detections.conf)):
    if conf < 0.3:
        continue

    x1, y1, x2, y2 = map(int, box)  # 🔥 manquant ici !
    padding = 5
    x1p = max(x1 + padding, 0)
    x2p = min(x2 - padding, img.shape[1])
    y1p = max(y1 + padding, 0)
    y2p = min(y2 - padding, img.shape[0])

    roi = img[y1p:y2p, x1p:x2p]

    cv2.imwrite(f"dossard_{i}.jpg", roi)

    # 🌀 Correction d’inclinaison
    deskewed, best_text = deskew_best_rotation(roi, max_angle=15)
    cv2.imwrite(f"dossard_{i}_deskewed.jpg", deskewed)

    if best_text:
        bib_numbers.append(best_text)
        print(f"📖 OCR optimisé dans dossard_{i} : {best_text}")
    else:
        print(f"📖 Aucun numéro valide trouvé dans dossard_{i}")



    # cv2.imwrite(f"dossard_{i}_deskewed.jpg", deskewed)

    # 🔲 Prétraitement pour OCR
    gray = cv2.cvtColor(deskewed, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    cv2.imwrite(f"dossard_{i}_thresh.jpg", thresh)

    # # 🔠 Tesseract OCR
    # 🔠 Tesseract OCR
    config = '--psm 6 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(thresh, config=config).strip()

    # # 🔍 Extraction de séquences de 4 à 6 chiffres
    # matches = re.findall(r"\d{4,6}", text)
    # if matches:
    #     best = max(matches, key=len)
    #     bib_numbers.append(best)
    #     print(f"📖 OCR filtré dans dossard_{i} : {best}")
    # else:
    #     print(f"📖 OCR (brut mais non valide) dans dossard_{i} : '{text}'")

    # 💾 Enregistrement des résultats OCR
    with open("resultats_bib.txt", "w") as f:
        for num in bib_numbers:
            f.write(num + "\n")

    print("✅ Résultats OCR enregistrés dans resultats_bib.txt")


    
