require('dotenv').config();
const app = require('./app');
const connectDB = require('./config/db');

const PORT = process.env.PORT || 5000;

// Connect to MongoDB
connectDB();

const server = app.listen(PORT, () => {
  console.log(`====================================================`);
  console.log(`🚀 IntentLens Server listening on http://localhost:${PORT}`);
  console.log(`📡 Connected to NLP Service at: ${process.env.NLP_SERVICE_URL || 'http://127.0.0.1:8000'}`);
  console.log(`====================================================`);
});

process.on('unhandledRejection', (err) => {
  console.error(`Unhandled Rejection Error: ${err.message}`);
  // Keep server alive, log error
});
