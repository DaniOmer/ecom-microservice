# Utilise une image officielle Node.js
FROM node:18

# Définir le dossier de travail dans le conteneur
WORKDIR /app

# Copier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier tout le reste du code
COPY . .

# Exposer le port 8081
EXPOSE 8081

# Démarrer l'application
CMD ["npm", "start"]