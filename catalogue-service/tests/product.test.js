const request = require('supertest');
const express = require('express');
const bodyParser = require('body-parser');
const ProductController = require('../controllers/ProductController');
const connectDB = require('../db');

const app = express();
app.use(bodyParser.json());

app.get('/products', ProductController.getAllProducts);
app.get('/products/:id', ProductController.getProductById);
app.post('/products', ProductController.createProduct);
app.put('/products/:id', ProductController.updateProduct);
app.delete('/products/:id', ProductController.deleteProduct);

beforeAll(async () => {
    await connectDB();
});

// Stocker l'id d'un produit créé pour les tests suivants
let createdProductId;

describe('Tests API /products', () => {

    test('POST /products -> devrait créer un nouveau produit', async () => {
        const response = await request(app)
            .post('/products')
            .send({
                name: "Test Produit",
                description: "Produit de test",
                price: 99.99,
                category: "Tests",
                images: ["https://test.com/image.jpg"]
            });
        expect(response.statusCode).toBe(201);
        expect(response.body).toHaveProperty('_id');
        createdProductId = response.body._id;
    });

    test('GET /products -> devrait retourner une liste de produits', async () => {
        const response = await request(app).get('/products');
        expect(response.statusCode).toBe(200);
        expect(Array.isArray(response.body)).toBe(true);
    });

    test('GET /products/:id -> devrait retourner le produit créé', async () => {
        const response = await request(app).get(`/products/${createdProductId}`);
        expect(response.statusCode).toBe(200);
        expect(response.body).toHaveProperty('name', "Test Produit");
    });

    test('PUT /products/:id -> devrait mettre à jour le produit', async () => {
        const response = await request(app)
            .put(`/products/${createdProductId}`)
            .send({
                name: "Produit Modifié",
                description: "Description modifiée",
                price: 199.99,
                category: "Tests Modifiés",
                images: ["https://testmodif.com/image.jpg"]
            });
        expect(response.statusCode).toBe(200);
        expect(response.body).toHaveProperty('name', "Produit Modifié");
    });

    test('DELETE /products/:id -> devrait supprimer le produit', async () => {
        const response = await request(app).delete(`/products/${createdProductId}`);
        expect(response.statusCode).toBe(200);
        expect(response.body).toHaveProperty('message', "Produit supprimé avec succès");
    });

});