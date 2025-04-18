const mongoose = require('mongoose');

const connectDB = async () => {
    try {
        await mongoose.connect('mongodb://localhost:27017/catalogue_db', {
            useNewUrlParser: true,
            useUnifiedTopology: true
        });
        console.log('✅ Connecté à MongoDB');
    } catch (err) {
        console.error('Erreur de connexion à MongoDB :', err);
        process.exit(1);
    }
};

module.exports = connectDB;