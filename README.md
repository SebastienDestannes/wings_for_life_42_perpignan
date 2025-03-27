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
│   ├── dossards_a_verifier/  # 🔍 Dossards non reconnus automatiquement
│   └── photos_resultats/     # 🖼️ (optionnel) Images annotées
├── runs/                     # 📆 Résultats d'entraînement YOLO (weights)
├── resultats_batch.txt       # ✅ Fichier contenant les dossards détectés
├── participants.json         # 📋 Données des participants (nom et passages)
├── a_verifier_manuellement.txt  # ❌ Liste des dossards à corriger manuellement
├── webcam_capture.py         # 📷 Script qui capture les images
├── analyser_images.py        # 🤖 Script qui analyse les images capturées
├── tri_d_une_photo.py        # 📸 Analyse une seule image (debug/test OCR)
├── tri_des_photos.py         # 🔁 Analyse continue des nouvelles photos
├── filtrer_resultats.py      # 🧹 Trie et filtre les résultats (matchs approximatifs)
├── verifier_manuellement.py  # 🧑‍🏫 Script pour correction manuelle des erreurs
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

### 🤖 2. Analyser les images capturées automatiquement

```bash
python analyser_images.py
```

> 📝 Les résultats sont sauvegardés dans : `resultats_batch.txt`

---

### ↻ 3. Ou analyser les images en continu (mode surveillance)

```bash
python tri_des_photos.py
```

Ce script surveille en boucle le dossier `photos/photos_brutes` et analyse les nouvelles images dès qu’elles arrivent.

---

### 🧹 4. Filtrer les résultats et corriger automatiquement les erreurs proches

```bash
python filtrer_resultats.py
```

Ce script ajoute les temps détectés pour les dossards présents dans `participants.json`. En cas d’erreur de lecture, il tente une correction approximative (ex : 7647 → 76477). Sinon, la photo est déplacée dans `photos/dossards_a_verifier`.

---

### 🧑‍🏫 5. Corriger manuellement les dossards restants

```bash
python verifier_manuellement.py
```

Les images avec dossards non reconnus sont affichées une par une. Tu peux entrer le bon numéro à la main. Le script met à jour `participants.json` et nettoie les photos traitées.

---

### 🧪 6. Tester une seule image pour debug

```bash
python tri_d_une_photo.py
```

Permet de tester une image spécifique pour vérifier les résultats OCR et les ajustements de rotation.

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