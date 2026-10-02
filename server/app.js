const express = require('express');
const cors = require('cors');
const errorHandler = require('./middleware/error.middleware');
const analysisRoutes = require('./routes/analysis.routes');

const app = express();

// Middleware
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'DELETE', 'PUT', 'PATCH', 'OPTIONS'],
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logger for academic/debugging visibility
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.originalUrl}`);
  next();
});

// API Routes
app.use('/api', analysisRoutes);

// Root informational endpoint
app.get('/', (req, res) => {
  res.json({
    service: 'IntentLens Express API Gateway',
    version: '1.0.0',
    description: 'Student Learning Intent Intelligence System Gateway',
    endpoints: {
      analyze: 'POST /api/analysis',
      history: 'GET /api/analysis',
      intents: 'GET /api/intents',
      health: 'GET /api/health',
    },
  });
});

// Global error handler
app.use(errorHandler);

module.exports = app;
