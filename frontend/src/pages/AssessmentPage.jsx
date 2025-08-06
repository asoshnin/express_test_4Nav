import React, { useState, useEffect } from 'react';
import Header from '../components/common/Header';
import ProgressBar from '../components/assessment/ProgressBar';
import QuestionDisplay from '../components/assessment/QuestionDisplay';
import LoadingSpinner from '../components/common/LoadingSpinner';
import apiService from '../services/api';

const AssessmentPage = ({ session, onComplete }) => {
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadNextQuestion();
  }, []);

  const loadNextQuestion = async () => {
    setLoading(true);
    setError(null);
    try {
      const question = await apiService.getQuestion(session.sessionId);
      setCurrentQuestion(question);
    } catch (error) {
      console.error('Failed to load question:', error);
      setError('Failed to load the next question. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = async (chosenStatementId) => {
    setSubmitting(true);
    try {
      await apiService.submitAnswer(
        session.sessionId,
        currentQuestion.questionNumber,
        chosenStatementId
      );

      // Check if this was the last question
      if (currentQuestion.questionNumber >= currentQuestion.totalQuestions) {
        // Assessment complete, generate report
        const report = await apiService.generateReport(session.sessionId);
        onComplete(report);
      } else {
        // Load next question
        loadNextQuestion();
      }
    } catch (error) {
      console.error('Failed to submit answer:', error);
      setError('Failed to submit your answer. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header currentPage="assessment" nickname={session?.nickname} />
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="card">
            <LoadingSpinner size="lg" text="Loading your assessment..." />
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header currentPage="assessment" nickname={session?.nickname} />
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="card text-center">
            <div className="text-red-600 mb-4">
              <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Something went wrong</h2>
            <p className="text-gray-600 mb-6">{error}</p>
            <button
              onClick={loadNextQuestion}
              className="btn-primary"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header currentPage="assessment" nickname={session?.nickname} />
      
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Progress Section */}
        <div className="mb-8">
          <ProgressBar
            current={currentQuestion?.questionNumber || 0}
            total={currentQuestion?.totalQuestions || 40}
          />
        </div>

        {/* Question Section */}
        <QuestionDisplay
          question={currentQuestion}
          onAnswer={handleAnswer}
          loading={submitting}
        />

        {/* Assessment Tips */}
        <div className="mt-8 card bg-blue-50 border-blue-200">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 mt-0.5">
              <svg className="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
            </div>
            <div>
              <h4 className="font-semibold text-blue-800 mb-1">Assessment Tips</h4>
              <ul className="text-blue-700 text-sm space-y-1">
                <li>• Choose the option that feels most natural to you</li>
                <li>• Don't overthink - go with your first instinct</li>
                <li>• There are no right or wrong answers</li>
                <li>• You can take breaks and return later</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AssessmentPage; 