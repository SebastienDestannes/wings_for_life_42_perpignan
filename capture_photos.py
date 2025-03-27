import cv2
import time
import os

# 📁 Dossier de sortie
output_dir = "photos/photos_brutes"
os.makedirs(output_dir, exist_ok=True)

# ⏱️ Intervalle de capture (en secondes)
INTERVAL = 0.5

# 📷 Démarrage de la webcam
cap = cv2.VideoCapture(0)
assert cap.isOpened(), "❌ Webcam non détectée"

print("📸 Capture toutes les 0.5 secondes - Appuie sur 'q' pour quitter")

last_capture = time.time()
img_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Erreur de lecture webcam")
        break

    now = time.time()
    if now - last_capture >= INTERVAL:
        last_capture = now
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/photo_{timestamp}_{img_count}.jpg"
        cv2.imwrite(filename, frame)
        print(f"✅ Image sauvegardée : {filename}")
        img_count += 1

    cv2.imshow("Webcam - Capture", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
