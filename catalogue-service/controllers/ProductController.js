const ProductRepository = require("../repositories/ProductRepository");
const axios = require("axios");

// GET /products
exports.getAllProducts = async (req, res) => {
  const products = await ProductRepository.findAll();
  res.json(products);
};

// GET /products/:id
exports.getProductById = async (req, res) => {
  try {
    const product = await ProductRepository.findById(req.params.id);
    if (!product) {
      return res.status(404).json({ message: "Produit non trouvé" });
    }
    res.json(product);
  } catch (err) {
    res.status(400).json({ message: "ID invalide" });
  }
};

// POST /products
exports.createProduct = async (req, res) => {
  const { name, description, price, category, images, quantity } = req.body;
  if (!name || !description || !price || !category || !quantity) {
    return res.status(400).json({
      message: "Tous les champs requis : name, description, price, category",
    });
  }
  const newProduct = await ProductRepository.create({
    name,
    description,
    price,
    category,
    images: images || [],
  });
  // Make api request to create inventory service
  const inventoryResponse = await axios.post(
    "http://inventory-service:8000/inventory/",
    {
      product_uid: newProduct._id,
      quantity_available: quantity,
      reserved_quantity: 0,
    }
  );
  console.log("Inventory service response:", inventoryResponse.data);
  res.status(201).json(newProduct);
};

// PUT /products/:id - Mise à jour d'un produit
exports.updateProduct = async (req, res) => {
  try {
    const updatedProduct = await ProductRepository.update(
      req.params.id,
      req.body
    );
    if (!updatedProduct) {
      return res.status(404).json({ message: "Produit non trouvé" });
    }
    res.json(updatedProduct);
  } catch (err) {
    console.error("Erreur lors de la mise à jour du produit :", err);
    res.status(400).json({ message: "ID invalide ou erreur de mise à jour" });
  }
};

// DELETE /products/:id - Suppression d'un produit
exports.deleteProduct = async (req, res) => {
  try {
    const deletedProduct = await ProductRepository.delete(req.params.id);
    if (!deletedProduct) {
      return res.status(404).json({ message: "Produit non trouvé" });
    }
    res.json({ message: "Produit supprimé avec succès" });
  } catch (err) {
    console.error("Erreur lors de la suppression du produit :", err);
    res.status(400).json({ message: "ID invalide" });
  }
};
