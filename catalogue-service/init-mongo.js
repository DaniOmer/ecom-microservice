db = db.getSiblingDB('catalogue_db');

// Create products collection if it doesn't exist
if (!db.getCollectionNames().includes('products')) {
    db.createCollection('products');
}

// Clear existing products
db.products.deleteMany({});

// Insert sample products
db.products.insertMany([
    {
        name: "Product 1",
        description: "This is product 1",
        price: 29.99,
        stock: 100,
        category: "Electronics"
    },
    {
        name: "Product 2",
        description: "This is product 2",
        price: 39.99,
        stock: 50,
        category: "Clothing"
    },
    {
        name: "Product 3",
        description: "This is product 3",
        price: 49.99,
        stock: 75,
        category: "Home"
    }
]);

print("MongoDB initialized with sample products");
