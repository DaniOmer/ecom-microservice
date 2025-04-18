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
├── docs/                   # Contient la documentation détaillée de chaque microservice
├── product-service/        # Microservice des produits
├── inventory-service/      # Microservice du stock
├── cart-service/           # Microservice du panier
├── order-service/          # Microservice des commandes
├── compose.yaml            # Orchestration des services
├── README.md               # Ce fichier
└── .env                    # Variables globales (ports, db, etc.)
```
