# Utiliser Miniconda comme image de base
FROM continuumio/miniconda3

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier environment.yml pour créer l'environnement Conda
COPY environment.yml /app/environment.yml

# Installer les dépendances système nécessaires pour PyQt et le serveur X11
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libegl1-mesa \
    libx11-dev \
    libxext6 \
    libxrender1 \
    libxrandr2 \
    libxkbcommon-x11-0 \
    libfontconfig1 \
    libfreetype6 \
    fonts-dejavu \
    libxcb1 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb-shm0 \
    libxcb-randr0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-util1 \
    libxcb-xv0 \
    libxcb-cursor0 \
    libdbus-1-3 \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# Créer l'environnement Conda
RUN conda env create -f /app/environment.yml

# Activer l'environnement Conda dans le shell
SHELL ["/bin/bash", "-c"]
RUN echo "source /opt/conda/etc/profile.d/conda.sh && conda activate Kicekifeqoa" >> ~/.bashrc

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Définir le PYTHONPATH
ENV PYTHONPATH=/app

# Définir la variable DISPLAY pour le serveur X11
ENV DISPLAY=host.docker.internal:0.0

# Définir le point d'entrée pour exécuter le script principal
CMD ["bash", "-c", "source /opt/conda/etc/profile.d/conda.sh && conda activate Kicekifeqoa && python /app/main.py"]
