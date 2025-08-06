import React from 'react';
import { Brain, BarChart3, Home } from 'lucide-react';

const Header = ({ currentPage, nickname }) => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Title */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-primary-600 rounded-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-semibold text-gray-900">
                AI Navigator Profiler
              </h1>
              {nickname && (
                <p className="text-sm text-gray-500">
                  Session: {nickname}
                </p>
              )}
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              {currentPage === 'assessment' && (
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-primary-600 rounded-full animate-pulse"></div>
                  <span>Assessment in Progress</span>
                </div>
              )}
              {currentPage === 'report' && (
                <div className="flex items-center space-x-2">
                  <BarChart3 className="w-4 h-4 text-green-600" />
                  <span>Report Generated</span>
                </div>
              )}
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header; 