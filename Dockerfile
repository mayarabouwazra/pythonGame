FROM python:3.9-slim

# Installer les dépendances système nécessaires pour pygame
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libtiff5-dev \
    libasound2-dev \
    && rm -rf /var/lib/apt/lists/*

# Créer un répertoire pour l'application
WORKDIR /app

RUN pip install --upgrade pip


# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=60 -r requirements.txt


# Copier le reste des fichiers de l'application
COPY . .


# Commande pour démarrer votre application
CMD ["python", "jeu.py"]
