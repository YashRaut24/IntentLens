const Analysis = require('../models/Analysis');
const nlpService = require('../services/nlp.service');
const mongoose = require('mongoose');

// @desc Analyze student query via NLP and store in DB
// @route POST /api/analysis
exports.createAnalysis = async (req, res, next) => {
  try {
    const { query, userId } = req.body;

    if (!query || typeof query !== 'string' || !query.trim()) {
      return res.status(400).json({
        success: false,
        error: 'Please describe what you want to learn before analyzing.',
      });
    }

    const trimmedQuery = query.trim();
    if (trimmedQuery.length < 3) {
      return res.status(400).json({
        success: false,
        error: 'Query is too short. Please provide a more descriptive learning query.',
      });
    }

    // Call Python FastAPI NLP Pipeline
    const nlpResult = await nlpService.analyzeQuery(trimmedQuery);

    const isUnclear = Boolean(nlpResult.is_unclear);
    const goal = nlpResult.goal ? { text: nlpResult.goal.text, topic: nlpResult.goal.topic } : null;
    const knownSkills = nlpResult.known_skills || nlpResult.knownSkills || [];
    const explicitGaps = nlpResult.explicit_gaps || nlpResult.explicitGaps || [];
    const potentialGaps = nlpResult.potential_gaps || nlpResult.potentialGaps || [];
    const learningLevel = nlpResult.learning_level || nlpResult.learningLevel || 'UNKNOWN';
    const learningContext = nlpResult.learning_context || nlpResult.learningContext || 'SKILL_DEVELOPMENT';
    const prerequisites = nlpResult.prerequisites || [];
    const knowledgeStates = (nlpResult.knowledge_states || nlpResult.knowledgeStates || []).map((ks) => ({
      concept: ks.concept,
      state: ks.state,
    }));
    const startingPoint = nlpResult.starting_point || nlpResult.startingPoint || null;

    // Prepare DB document
    const analysisDoc = {
      userId: userId || 'anonymous-student',
      query: trimmedQuery,
      isUnclear,
      message: nlpResult.message || null,
      goal,
      knownSkills,
      explicitGaps,
      potentialGaps,
      topics: nlpResult.topics || [],
      relatedConcepts: nlpResult.related_concepts || [],
      keywords: nlpResult.keywords || [],
      learningLevel,
      learningContext,
      prerequisites,
      knowledgeStates,
      startingPoint,
      intent: nlpResult.intent
        ? {
            name: nlpResult.intent.name,
            label: nlpResult.intent.label,
            confidence: nlpResult.intent.confidence,
          }
        : null,
      confidence: nlpResult.confidence || 85,
      confidenceLabel: nlpResult.confidence_label || 'MEDIUM',
      semanticSimilarity: nlpResult.semantic_match
        ? {
            intent: nlpResult.semantic_match.intent,
            similarity: nlpResult.semantic_match.similarity,
          }
        : null,
      explanation: nlpResult.explanation || (startingPoint ? startingPoint.reason : ''),
    };

    let savedRecord = null;
    if (mongoose.connection.readyState === 1) {
      savedRecord = await Analysis.create(analysisDoc);
    } else {
      // Fallback if Mongo is down: return transient analysis with a generated id
      savedRecord = { ...analysisDoc, _id: 'temp-' + Date.now(), createdAt: new Date().toISOString() };
    }

    return res.status(201).json({
      success: true,
      data: savedRecord,
      nlpRaw: nlpResult,
    });
  } catch (error) {
    next(error);
  }
};

// @desc Get all analyses
// @route GET /api/analysis
exports.getAnalyses = async (req, res, next) => {
  try {
    if (mongoose.connection.readyState !== 1) {
      return res.status(200).json({
        success: true,
        count: 0,
        data: [],
        warning: 'Database offline, returning empty history',
      });
    }

    const limit = parseInt(req.query.limit, 10) || 50;
    const analyses = await Analysis.find().sort({ createdAt: -1 }).limit(limit);

    return res.status(200).json({
      success: true,
      count: analyses.length,
      data: analyses,
    });
  } catch (error) {
    next(error);
  }
};

// @desc Get single analysis by ID
// @route GET /api/analysis/:id
exports.getAnalysisById = async (req, res, next) => {
  try {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid analysis ID format',
      });
    }

    const analysis = await Analysis.findById(id);
    if (!analysis) {
      return res.status(404).json({
        success: false,
        error: 'Analysis record not found',
      });
    }

    return res.status(200).json({
      success: true,
      data: analysis,
    });
  } catch (error) {
    next(error);
  }
};

// @desc Delete single analysis by ID
// @route DELETE /api/analysis/:id
exports.deleteAnalysisById = async (req, res, next) => {
  try {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid analysis ID format',
      });
    }

    const deleted = await Analysis.findByIdAndDelete(id);
    if (!deleted) {
      return res.status(404).json({
        success: false,
        error: 'Analysis record not found to delete',
      });
    }

    return res.status(200).json({
      success: true,
      message: 'Analysis record deleted successfully',
      data: { id },
    });
  } catch (error) {
    next(error);
  }
};

// @desc Clear all analyses
// @route DELETE /api/analysis
exports.clearAllAnalyses = async (req, res, next) => {
  try {
    if (mongoose.connection.readyState !== 1) {
      return res.status(200).json({
        success: true,
        message: 'Database is not connected, history cleared',
      });
    }

    const result = await Analysis.deleteMany({});
    return res.status(200).json({
      success: true,
      message: 'All analysis history successfully cleared',
      deletedCount: result.deletedCount,
    });
  } catch (error) {
    next(error);
  }
};

// @desc Get intent taxonomy from NLP
// @route GET /api/intents
exports.getIntents = async (req, res, next) => {
  try {
    const intentsData = await nlpService.getIntents();
    return res.status(200).json({
      success: true,
      data: intentsData,
    });
  } catch (error) {
    next(error);
  }
};

// @desc Health check
// @route GET /api/health
exports.getHealth = async (req, res) => {
  const nlpHealth = await nlpService.checkHealth();
  const dbStatus = mongoose.connection.readyState === 1 ? 'connected' : 'disconnected';

  res.status(200).json({
    status: 'online',
    serverTime: new Date().toISOString(),
    database: {
      status: dbStatus,
    },
    nlpService: nlpHealth,
  });
};
