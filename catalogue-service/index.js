const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const connectDB = require('./db');
const ProductController = require('./controllers/ProductController');

const app = express();
const port = 8081;

app.use(cors());
app.use(bodyParser.json());

connectDB();

// Routes
app.get('/products', ProductController.getAllProducts);
app.get('/products/:id', ProductController.getProductById);
app.post('/products', ProductController.createProduct);
app.put('/products/:id', ProductController.updateProduct);
app.delete('/products/:id', ProductController.deleteProduct);

app.listen(port, () => {
    console.log(`Catalogue service écoute sur http://localhost:${port}`);
});
