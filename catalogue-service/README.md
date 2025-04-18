# Catalog Service

This is a microservice for managing product catalog in the e-commerce application.

## Features

- RESTful API for product management
- MongoDB database for product storage
- Docker containerization

## API Endpoints

- `GET /products` - Get all products
- `GET /products/:id` - Get a product by ID
- `POST /products` - Create a new product
- `PUT /products/:id` - Update a product
- `DELETE /products/:id` - Delete a product

## Development

### Prerequisites

- Node.js
- MongoDB
- Docker and Docker Compose

### Running Locally

1. Install dependencies:
   ```
   npm install
   ```

2. Start the service:
   ```
   npm start
   ```

### Running with Docker Compose

```
docker-compose up -d
```

## Environment Variables

- `PORT` - Port to run the service on (default: 3000)
- `MONGO_URI` - MongoDB connection string (default: mongodb://mongodb:27017/catalogue_db)
