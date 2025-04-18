const Product = require('../models/Product');

class ProductRepository {
    async findAll() {
        return await Product.find();
    }

    async findById(id) {
        return await Product.findById(id);
    }

    async create(productData) {
        const product = new Product(productData);
        return await product.save();
    }

    async update(id, updateData) {
        return await Product.findByIdAndUpdate(id, updateData, { new: true, runValidators: true });
    }

    async delete(id) {
        return await Product.findByIdAndDelete(id);
    }
}

module.exports = new ProductRepository();