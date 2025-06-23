FROM node:18

# Installer Python 3, pip et venv
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers
COPY . .

# Créer et activer l'environnement virtuel Python, puis installer les dépendances
RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Ajouter le venv au PATH
ENV PATH="/opt/venv/bin:$PATH"

# Installer les dépendances Node.js
RUN npm install

# Démarrer l'application Node.js
CMD ["npm", "start"]
