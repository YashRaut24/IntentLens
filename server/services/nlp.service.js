const axios = require('axios');

const NLP_BASE_URL = process.env.NLP_SERVICE_URL || 'http://127.0.0.1:8000';

class NLPService {
  constructor() {
    this.client = axios.create({
      baseURL: NLP_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async analyzeQuery(text) {
    try {
      const response = await this.client.post('/api/analyze', { text });
      return response.data;
    } catch (error) {
      if (error.response) {
        throw new Error(error.response.data?.detail || 'NLP Service returned an error');
      } else if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
        throw new Error('NLP Service is unreachable. Ensure the FastAPI microservice is running on port 8000.');
      } else {
        throw new Error(`NLP Service error: ${error.message}`);
      }
    }
  }

  async getIntents() {
    try {
      const response = await this.client.get('/api/intents');
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch intents from NLP service: ${error.message}`);
    }
  }

  async checkHealth() {
    try {
      const response = await this.client.get('/api/health');
      return response.data;
    } catch (error) {
      return { status: 'down', error: error.message };
    }
  }
}

module.exports = new NLPService();
