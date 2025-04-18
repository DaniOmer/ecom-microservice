# 🛍️ E-Commerce Microservices

Ce projet est une architecture e-commerce basée sur des microservices, développée avec Node.js (Javascript), PHP et FastAPI (Python). Chaque service est isolé, possède sa propre base de données, et communique via HTTP (ou événements si étendu).

---

## 🚀 Services inclus

| Service                     | Description                                                    |
| --------------------------- | -------------------------------------------------------------- |
| **Product Catalog Service** | Gère les produits, catégories, descriptions, prix, images      |
| **Inventory Service**       | Gère les niveaux de stock, les réservations de stock           |
| **Cart Service**            | Gère les paniers utilisateur (ajout, suppression, mise à jour) |
| **Order Service**           | Gère la création de commandes, leur statut, et historique      |

---

## 🧱 Structure du projet

```bash
ecommerce-microservices/
│
├── catalogue-service/      # Microservice du catalogue (Node.js, MongoDB)
│   ├── controllers/        # Contrôleurs pour gérer les requêtes API
│   ├── models/             # Modèles de données Mongoose
│   ├── repositories/       # Couche d'accès aux données
│   ├── index.js            # Point d'entrée de l'application
│   └── db.js               # Configuration de la base de données
│
├── order-service/          # Microservice des commandes (PHP, PostgreSQL)
│   ├── config/             # Configuration de la base de données
│   ├── db/                 # Scripts d'initialisation de la base de données
│   ├── index.php           # Point d'entrée de l'API
│   └── OrderService.php    # Logique métier des commandes
│
├── compose.yaml            # Orchestration des services
├── README.md               # Ce fichier
└── .env.example            # Exemple de variables d'environnement
```

---

## 🚀 Comment exécuter les microservices

### Prérequis

- Docker et Docker Compose installés sur votre machine
- Git pour cloner le dépôt

### Étapes pour démarrer les services

1. **Cloner le dépôt**

```bash
git clone <url-du-depot>
cd ecom-microservice
```

2. **Lancer les services avec Docker Compose**

```bash
docker compose up -d
```

Cette commande va:
- Construire l'image du service de catalogue (catalogue-service) avec Node.js et MongoDB
- Construire l'image du service de commandes (order-service) avec PHP et PostgreSQL
- Démarrer le service de catalogue (catalogue-service) sur le port 8081
- Démarrer le service de commandes (order-service) sur le port 8082
- Démarrer la base de données MongoDB pour le service de catalogue
- Démarrer la base de données PostgreSQL pour le service de commandes
- Démarrer Adminer (interface d'administration de base de données PostgreSQL) sur le port 8083

3. **Vérifier que les services sont en cours d'exécution**

```bash
docker compose ps
```

### Tester les API

#### Service de catalogue (Catalog Service)

Accéder à tous les produits:
```bash
curl http://localhost:8081/products
```

Accéder à un produit spécifique (remplacer `[id]` par l'ID MongoDB du produit):
```bash
curl http://localhost:8081/products/[id]
```

Exemple de réponse:
```json
{
  "_id": "68024bd1ca003321a9d861e0",
  "name": "Product 1",
  "description": "This is product 1",
  "price": 29.99,
  "stock": 100,
  "category": "Electronics",
  "createdAt": "2025-04-18T12:56:21.300Z"
}
```

Créer un nouveau produit:
```bash
curl -X POST http://localhost:8081/products \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Nouveau Produit",
       "description": "Description du nouveau produit",
       "price": 59.99,
       "stock": 25,
       "category": "Electronics"
     }'
```

Mettre à jour un produit existant:
```bash
curl -X PUT http://localhost:8081/products/[id] \
     -H "Content-Type: application/json" \
     -d '{
       "price": 69.99,
       "stock": 30
     }'
```

Supprimer un produit:
```bash
curl -X DELETE http://localhost:8081/products/[id]
```

#### Service de commandes (Order Service)

Créer une commande (utiliser les IDs MongoDB des produits):
```bash
curl -X POST http://localhost:8082/orders \
     -H "Content-Type: application/json" \
     -d '{"productIds": ["68024bd1ca003321a9d861e0", "68024bd1ca003321a9d861e1"]}'
```

Exemple de réponse:
```json
{
  "id": 1,
  "created_at": "2025-04-18 12:57:17.047848",
  "total": "69.98",
  "products": [
    {
      "product_id": "68024bd1ca003321a9d861e0",
      "product_name": "Product 1",
      "price": "29.99"
    },
    {
      "product_id": "68024bd1ca003321a9d861e1",
      "product_name": "Product 2",
      "price": "39.99"
    }
  ]
}
```

Récupérer une commande par ID:
```bash
curl http://localhost:8082/orders/1
```

### Intégration entre les services

Le système fonctionne de la manière suivante:

1. Le **Service de catalogue** gère les produits dans MongoDB
2. Le **Service de commandes** récupère les informations des produits depuis le Service de catalogue lors de la création d'une commande
3. Le Service de commandes calcule le prix total de la commande en additionnant les prix des produits
4. Les données de commande sont stockées dans PostgreSQL

Flux de création d'une commande:
```
Client → POST /orders avec IDs de produits → Service de commandes → 
  → Récupère les détails des produits depuis le Service de catalogue →
  → Calcule le total → Enregistre la commande → Retourne la commande créée
```

### Tests automatisés

Le projet inclut un script de test cross-platform qui vérifie le bon fonctionnement des services et leur intégration. Ce script fonctionne sur tous les systèmes d'exploitation (Windows, Mac, Linux).

#### Prérequis pour les tests

- Node.js installé sur votre machine
- Les services doivent être en cours d'exécution (`docker compose up -d`)

#### Exécuter les tests

```bash
# Exécuter le script de test Node.js (fonctionne sur tous les systèmes)
node test-microservices.js
```

Le script effectue les tests suivants:
1. Vérifie que les services sont en cours d'exécution
2. Teste les opérations CRUD du service de catalogue
3. Teste la création de commandes avec un ou plusieurs produits
4. Vérifie que le prix total est correctement calculé
5. Nettoie les données de test créées

#### Exemple de sortie de test

```
==== Testing Microservices ====

This script will test the catalog and order services

==== Checking if services are running ====

✓ Catalog service is running
✓ Order service is running

==== Testing Catalog Service ====

Getting all products...
✓ Get all products
Creating a new product...
{
  "_id": "60f1a2b3c4d5e6f7g8h9i0j1",
  "name": "Test Product",
  "description": "A test product created by the test script",
  "price": 49.99,
  "stock": 42,
  "category": "Test"
}
✓ Create product
Getting product by ID...
✓ Get product by ID
Updating product...
✓ Update product

==== Testing Order Service ====

Creating an order with a single product...
✓ Create order with single product
Checking total price...
✓ Total price is correct for single product order

==== Test Summary ====

All tests completed successfully!
Tests passed: 7
Tests failed: 0

The catalog service and order service are working together.
The order service can fetch product information from the catalog service and calculate the total price correctly.
```

### Dépannage

Si vous rencontrez des problèmes:

1. **Vérifiez que tous les services sont en cours d'exécution**:
   ```bash
   docker compose ps
   ```

2. **Consultez les logs des services**:
   ```bash
   docker compose logs catalog-service
   docker compose logs order-service
   ```

3. **Exécutez le script de test automatisé**:
   ```bash
   node test-microservices.js
   ```

4. **Problèmes courants**:
   - Assurez-vous d'utiliser les IDs MongoDB (chaînes de caractères) pour les produits lors de la création de commandes
   - Vérifiez que les services peuvent communiquer entre eux (le service de commandes doit pouvoir accéder au service de catalogue)

### Accéder aux bases de données

#### PostgreSQL (Service de commandes)

Vous pouvez accéder à l'interface Adminer pour gérer la base de données PostgreSQL:
1. Ouvrez votre navigateur et accédez à `http://localhost:8083`
2. Connectez-vous avec les informations suivantes:
   - Système: PostgreSQL
   - Serveur: postgres
   - Utilisateur: orders_user
   - Mot de passe: orders_password
   - Base de données: orders_db

#### MongoDB (Service de catalogue)

MongoDB est accessible sur le port 27017. Vous pouvez utiliser MongoDB Compass ou un autre outil pour vous y connecter:
- URI de connexion: `mongodb://localhost:27017/catalogue_db`

### Arrêter les services

Pour arrêter tous les services:
```bash
docker compose down
```

Pour arrêter les services et supprimer les volumes (cela effacera toutes les données):
```bash
docker compose down -v
```
