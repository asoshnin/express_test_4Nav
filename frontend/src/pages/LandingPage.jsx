import React, { useState } from 'react';
import { Brain, ArrowRight, Users, BarChart3, Download } from 'lucide-react';
import apiService from '../services/api';

const LandingPage = ({ onStartAssessment }) => {
  const [loading, setLoading] = useState(false);

  const handleStartAssessment = async () => {
    setLoading(true);
    try {
      const session = await apiService.startAssessment();
      onStartAssessment(session);
    } catch (error) {
      console.error('Failed to start assessment:', error);
      // You could add error handling UI here
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-blue-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="w-20 h-20 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-6">
            <Brain className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            AI Navigator Profiler
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Discover your unique approach to AI navigation and development. 
            Take our scientifically-grounded assessment to understand your 
            cognitive strengths and professional archetype.
          </p>
          <button
            onClick={handleStartAssessment}
            disabled={loading}
            className="btn-primary text-lg px-8 py-4 flex items-center space-x-2 mx-auto"
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Starting Assessment...</span>
              </>
            ) : (
              <>
                <span>Start Your Assessment</span>
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>
        </div>

        {/* Features Section */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          <div className="card text-center">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Brain className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Scientific Foundation
            </h3>
            <p className="text-gray-600">
              Based on established psychometric research with 11 core constructs 
              measured across 3 professional archetypes.
            </p>
          </div>

          <div className="card text-center">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Users className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Personalized Insights
            </h3>
            <p className="text-gray-600">
              Receive detailed, AI-generated reports tailored to your unique 
              cognitive profile and professional preferences.
            </p>
          </div>

          <div className="card text-center">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Download className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Downloadable Reports
            </h3>
            <p className="text-gray-600">
              Keep your assessment results with downloadable Markdown reports 
              for personal reference and professional development.
            </p>
          </div>
        </div>

        {/* Assessment Info */}
        <div className="card bg-gradient-to-r from-gray-50 to-gray-100">
          <div className="text-center">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              What to Expect
            </h2>
            <div className="grid md:grid-cols-2 gap-6 text-left">
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Assessment Process</h3>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                    <span>40 carefully crafted question pairs</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                    <span>Takes approximately 15-20 minutes</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                    <span>Anonymous and confidential</span>
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Your Results</h3>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                    <span>Primary and secondary archetype identification</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                    <span>Detailed cognitive profile analysis</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                    <span>Actionable development recommendations</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage; 