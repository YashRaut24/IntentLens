const mongoose = require('mongoose');

const KnowledgeStateSchema = new mongoose.Schema(
  {
    concept: { type: String, required: true },
    state: {
      type: String,
      enum: ['KNOWN', 'EXPLICIT_GAP', 'POTENTIAL_GAP', 'TARGET', 'RELATED'],
      required: true,
    },
  },
  { _id: false }
);

const AnalysisSchema = new mongoose.Schema(
  {
    userId: {
      type: String,
      default: 'anonymous-student',
      index: true,
    },
    query: {
      type: String,
      required: [true, 'Query text is required'],
      trim: true,
    },
    isUnclear: {
      type: Boolean,
      default: false,
    },
    message: {
      type: String,
      default: null,
    },
    goal: {
      text: { type: String },
      topic: { type: String },
    },
    knownSkills: {
      type: [String],
      default: [],
    },
    explicitGaps: {
      type: [String],
      default: [],
    },
    potentialGaps: {
      type: [String],
      default: [],
    },
    topics: {
      type: [String],
      default: [],
    },
    relatedConcepts: {
      type: [String],
      default: [],
    },
    keywords: {
      type: [String],
      default: [],
    },
    learningLevel: {
      type: String,
      enum: ['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'UNKNOWN'],
      default: 'UNKNOWN',
    },
    learningContext: {
      type: String,
      default: 'SKILL_DEVELOPMENT',
    },
    prerequisites: {
      type: [String],
      default: [],
    },
    knowledgeStates: {
      type: [KnowledgeStateSchema],
      default: [],
    },
    startingPoint: {
      title: { type: String },
      reason: { type: String },
    },
    intent: {
      name: { type: String },
      label: { type: String },
      confidence: { type: Number },
    },
    confidence: {
      type: Number,
      required: true,
    },
    confidenceLabel: {
      type: String,
      enum: ['HIGH', 'MEDIUM', 'LOW'],
      default: 'MEDIUM',
    },
    semanticSimilarity: {
      intent: { type: String },
      similarity: { type: Number },
    },
    explanation: {
      type: String,
      required: true,
    },
  },
  {
    timestamps: true,
    collection: 'analyses',
  }
);

AnalysisSchema.index({ createdAt: -1 });

module.exports = mongoose.model('Analysis', AnalysisSchema);
