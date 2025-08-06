import React, { useState } from 'react';
import { CheckCircle, Circle } from 'lucide-react';

const QuestionDisplay = ({ question, onAnswer, loading = false }) => {
  const [selectedOption, setSelectedOption] = useState(null);

  const handleOptionClick = (optionId) => {
    if (loading) return;
    setSelectedOption(optionId);
  };

  const handleSubmit = () => {
    if (selectedOption && !loading) {
      onAnswer(selectedOption);
    }
  };

  if (!question) {
    return (
      <div className="card animate-pulse">
        <div className="h-6 bg-gray-200 rounded mb-4"></div>
        <div className="space-y-3">
          <div className="h-16 bg-gray-200 rounded"></div>
          <div className="h-16 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="card animate-fade-in">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-2">
          Choose the statement that best describes you:
        </h2>
        <p className="text-gray-600">
          Select the option that resonates most with your natural tendencies and preferences.
        </p>
      </div>

      <div className="space-y-4">
        {Object.entries(question.statements).map(([optionId, statement]) => (
          <button
            key={optionId}
            onClick={() => handleOptionClick(optionId)}
            disabled={loading}
            className={`w-full p-6 text-left rounded-lg border-2 transition-all duration-200 ${
              selectedOption === optionId
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
            } ${loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
          >
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 mt-1">
                {selectedOption === optionId ? (
                  <CheckCircle className="w-6 h-6 text-primary-600" />
                ) : (
                  <Circle className="w-6 h-6 text-gray-400" />
                )}
              </div>
              <div className="flex-1">
                <p className="text-gray-900 font-medium leading-relaxed">
                  {statement.text}
                </p>
              </div>
            </div>
          </button>
        ))}
      </div>

      <div className="mt-8 flex justify-end">
        <button
          onClick={handleSubmit}
          disabled={!selectedOption || loading}
          className={`btn-primary ${
            !selectedOption || loading
              ? 'opacity-50 cursor-not-allowed'
              : ''
          }`}
        >
          {loading ? (
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span>Submitting...</span>
            </div>
          ) : (
            'Continue'
          )}
        </button>
      </div>
    </div>
  );
};

export default QuestionDisplay; 