# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: sdestann <sdestann@tudent.42perpignan.f    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/03/27 14:28:43 by sdestann          #+#    #+#              #
#    Updated: 2025/03/28 08:37:51 by sdestann         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# 📦 Environnement Python
VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

# 📁 Dossiers
SRC := .
PHOTOS := photos/photos_brutes

# 📄 Fichiers
REQUIREMENTS := requirements.txt

# 🧪 Création de l'environnement virtuel + install des dépendances
install: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate:
	@echo "📦 Création de l'environnement virtuel..."
	python3 -m venv $(VENV_DIR)
	@echo "📥 Installation des dépendances..."
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS)
	@echo "✅ Environnement prêt. Active-le avec: source $(VENV_DIR)/bin/activate"

# 🧪 Lancer la capture d'images (webcam)
capture:
	@echo "📷 Lancement de la capture d'images toutes les 0.5 secondes..."
	$(PYTHON) capture_photos.py

# 🔍 Lancer l'analyse des images avec OCR
analyser:
	@echo "🤖 Lancement de l’analyse OCR des photos brutes..."
	$(PYTHON) tri_des_photos.py

# 🧼 Nettoyage des photos brutes
clean:
	@echo "🧹 Suppression des photos brutes..."
	rm -f $(PHOTOS)/*.jpg

# 🧪 Filtrage des résultats OCR
filtrer:
	@echo "📊 Lancement du filtre de résultats OCR (comparaison avec JSON)..."
	$(PYTHON) filtrer_resultats.py

# Vérification manuelle des dossards inconnus
verifier:
	@echo "📊 Vérification manuelle des dossards inconnus..."
	$(PYTHON) verifier_manuellement.py


# 💬 Aide
help:
	@echo "🛠️ Commandes disponibles :"
	@echo "  make install     → Créer l'environnement virtuel et installer les dépendances"
	@echo "  make capture     → Lancer la capture webcam d'images toutes les 0.5s"
	@echo "  make analyser    → Lancer le traitement OCR des images"
	@echo "  make filtrer     → Filtrer les résultats OCR avec la base de dossards"
	@echo "  make clean       → Supprimer les photos capturées"

