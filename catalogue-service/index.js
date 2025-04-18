const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const connectDB = require('./db');
const ProductController = require('./controllers/ProductController');

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Connect to MongoDB
connectDB();

// Routes
app.get('/products', ProductController.getAllProducts);
app.get('/products/:id', ProductController.getProductById);
app.post('/products', ProductController.createProduct);
app.put('/products/:id', ProductController.updateProduct);
app.delete('/products/:id', ProductController.deleteProduct);

// Start server
app.listen(PORT, () => {
  console.log(`Catalog service running on port ${PORT}`);
});
