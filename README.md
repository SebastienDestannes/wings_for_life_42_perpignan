## 🏃‍♂️ Détection de dossards (OCR) sur une course à pied

Ce projet permet de **suivre automatiquement les coureurs** en détectant leurs **numéros de dossards** sur des images capturées toutes les 0.5 secondes depuis une webcam.

> 📷 **YOLO** est utilisé pour détecter les dossards,  
> 🔠 **Tesseract OCR** pour lire les numéros sur l’image.

---

### 📁 Arborescence du projet

```
.
├── photos/
│   ├── photos_brutes/        # 📸 Images capturées automatiquement
│   └── photos_resultats/     # 🖼️ (optionnel) Images annotées
├── runs/                     # 📦 Résultats d'entraînement YOLO (weights)
├── resultats_batch.txt       # ✅ Fichier contenant les dossards détectés
├── webcam_capture.py         # 📷 Script qui capture les images
├── analyser_images.py        # 🤖 Script qui analyse les images capturées
└── README.md
```

---

### 🔧 Prérequis

- Python 3.9+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installé et accessible dans le PATH
- OpenCV
- PyTesseract
- Ultralytics (YOLOv8)

---

### ⚙️ Installation

```bash
# Créer un environnement virtuel (optionnel)
python3 -m venv monenv
source monenv/bin/activate

# Installer les dépendances Python
pip install -r requirements.txt
```

#### Exemple de `requirements.txt` :

```txt
ultralytics
opencv-python
pytesseract
```

---

### 🚀 1. Lancer la capture webcam

Le script capture **une image toutes les 0.5 secondes** et les stocke dans `photos/photos_brutes`.

```bash
python webcam_capture.py
```

> ⏹️ Appuyer sur **q** pour quitter

---

### 🤖 2. Lancer l’analyse automatique des images

Ce script lit toutes les nouvelles images dans `photos/photos_brutes/` et en extrait les numéros de dossards.

```bash
python analyser_images.py
```

> 📝 Les résultats sont sauvegardés dans : `resultats_batch.txt`

---

### 📊 Format du fichier de sortie (`resultats_batch.txt`)

```csv
photo_20250327_153201_1.jpg,76477
photo_20250327_153202_2.jpg,100909
...
```

---

### 📌 Remarques

- Le modèle YOLO doit être déjà entraîné et stocké dans :  
  `runs/detect/train/weights/best.pt`
- La détection fonctionne même si les dossards sont **inclinés** (rotation auto)

---

### 📚 Crédits

- [YOLOv8 - Ultralytics](https://github.com/ultralytics/ultralytics)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- Captures et dataset inspirés de [Roboflow](https://roboflow.com/)

### Models

- by Marco Cheung (https://universe.roboflow.com/marco-cheung/bib-number-labeling)

---