const ProductRepository = require('../repositories/ProductRepository');

// GET /products
exports.getAllProducts = async (req, res) => {
    try {
        const products = await ProductRepository.findAll();
        res.json(products);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

// GET /products/:id
exports.getProductById = async (req, res) => {
    try {
        const product = await ProductRepository.findById(req.params.id);
        if (!product) {
            return res.status(404).json({ error: 'Product not found' });
        }
        res.json(product);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

// POST /products
exports.createProduct = async (req, res) => {
    try {
        const product = await ProductRepository.create(req.body);
        res.status(201).json(product);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

// PUT /products/:id
exports.updateProduct = async (req, res) => {
    try {
        const product = await ProductRepository.update(req.params.id, req.body);
        if (!product) {
            return res.status(404).json({ error: 'Product not found' });
        }
        res.json(product);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

// DELETE /products/:id
exports.deleteProduct = async (req, res) => {
    try {
        const result = await ProductRepository.delete(req.params.id);
        if (!result) {
            return res.status(404).json({ error: 'Product not found' });
        }
        res.status(204).send();
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};
