import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service class for all backend endpoints
class ApiService {
  // Start assessment and get session
  async startAssessment() {
    try {
      const response = await api.post('/assessment');
      return response.data;
    } catch (error) {
      console.error('Error starting assessment:', error);
      throw error;
    }
  }

  // Get next question
  async getQuestion(sessionId) {
    try {
      const response = await api.get(`/assessment/${sessionId}/question`);
      return response.data;
    } catch (error) {
      console.error('Error getting question:', error);
      throw error;
    }
  }

  // Submit answer
  async submitAnswer(sessionId, questionNumber, chosenStatementId) {
    try {
      const response = await api.post(`/assessment/${sessionId}/answer`, {
        questionNumber,
        chosenStatementId,
      });
      return response.data;
    } catch (error) {
      console.error('Error submitting answer:', error);
      throw error;
    }
  }

  // Get session status
  async getSessionStatus(sessionId) {
    try {
      const response = await api.get(`/assessment/${sessionId}/status`);
      return response.data;
    } catch (error) {
      console.error('Error getting session status:', error);
      throw error;
    }
  }

  // Generate report
  async generateReport(sessionId) {
    try {
      const response = await api.get(`/assessment/${sessionId}/report`);
      return response.data;
    } catch (error) {
      console.error('Error generating report:', error);
      throw error;
    }
  }

  // Download report
  async downloadReport(sessionId) {
    try {
      const response = await api.get(`/assessment/${sessionId}/report/download`, {
        responseType: 'blob',
      });
      
      // Create download link
      const blob = new Blob([response.data], { type: 'text/markdown' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `navigator-report-${sessionId}.md`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      return { success: true };
    } catch (error) {
      console.error('Error downloading report:', error);
      throw error;
    }
  }

  // Submit contact information
  async submitContact(sessionId, email) {
    try {
      const response = await api.post(`/assessment/${sessionId}/contact`, {
        email,
      });
      return response.data;
    } catch (error) {
      console.error('Error submitting contact:', error);
      throw error;
    }
  }

  // Get analytics
  async getAnalytics(period = '7d') {
    try {
      const response = await api.get(`/analytics?period=${period}`);
      return response.data;
    } catch (error) {
      console.error('Error getting analytics:', error);
      throw error;
    }
  }

  // Health check
  async healthCheck() {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  }
}

export default new ApiService(); 