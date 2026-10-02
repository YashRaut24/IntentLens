const express = require('express');
const router = express.Router();
const {
  createAnalysis,
  getAnalyses,
  getAnalysisById,
  deleteAnalysisById,
  clearAllAnalyses,
  getIntents,
  getHealth,
} = require('../controllers/analysis.controller');

// Analysis Endpoints
router.route('/analysis')
  .post(createAnalysis)
  .get(getAnalyses)
  .delete(clearAllAnalyses);

router.route('/analysis/:id')
  .get(getAnalysisById)
  .delete(deleteAnalysisById);

// Intent catalog & Health
router.get('/intents', getIntents);
router.get('/health', getHealth);

module.exports = router;
