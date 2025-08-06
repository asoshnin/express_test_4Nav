import React, { useState } from 'react';
import { Download, Mail, CheckCircle, AlertCircle, TrendingUp } from 'lucide-react';
import apiService from '../../services/api';

const ReportViewer = ({ report, sessionId, onDownload, onContact }) => {
  const [email, setEmail] = useState('');
  const [contactSubmitted, setContactSubmitted] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [submittingContact, setSubmittingContact] = useState(false);

  const handleDownload = async () => {
    setDownloading(true);
    try {
      await apiService.downloadReport(sessionId);
      onDownload?.();
    } catch (error) {
      console.error('Download failed:', error);
    } finally {
      setDownloading(false);
    }
  };

  const handleContactSubmit = async (e) => {
    e.preventDefault();
    if (!email || contactSubmitted) return;

    setSubmittingContact(true);
    try {
      await apiService.submitContact(sessionId, email);
      setContactSubmitted(true);
      onContact?.();
    } catch (error) {
      console.error('Contact submission failed:', error);
    } finally {
      setSubmittingContact(false);
    }
  };

  if (!report) {
    return (
      <div className="card animate-pulse">
        <div className="h-8 bg-gray-200 rounded mb-4"></div>
        <div className="space-y-3">
          <div className="h-4 bg-gray-200 rounded"></div>
          <div className="h-4 bg-gray-200 rounded"></div>
          <div className="h-4 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Report Header */}
      <div className="card">
        <div className="text-center mb-6">
          <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <TrendingUp className="w-8 h-8 text-primary-600" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Your AI Navigator Profile
          </h1>
          <p className="text-gray-600">
            Discover your unique approach to AI navigation and development
          </p>
        </div>

        {/* Primary Archetype */}
        <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-lg p-6 mb-6">
          <div className="flex items-center space-x-3 mb-3">
            <CheckCircle className="w-6 h-6 text-primary-600" />
            <h2 className="text-xl font-semibold text-gray-900">
              Your Primary Archetype
            </h2>
          </div>
          <h3 className="text-2xl font-bold text-primary-700 mb-2">
            {report.primaryArchetype}
          </h3>
          <p className="text-gray-700 leading-relaxed">
            {report.reportNarrative}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4">
          <button
            onClick={handleDownload}
            disabled={downloading}
            className="btn-primary flex items-center justify-center space-x-2"
          >
            <Download className="w-5 h-5" />
            <span>{downloading ? 'Downloading...' : 'Download Report'}</span>
          </button>
        </div>
      </div>

      {/* Contact Form */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Mail className="w-6 h-6 text-gray-600" />
          <h3 className="text-lg font-semibold text-gray-900">
            Stay Connected
          </h3>
        </div>
        <p className="text-gray-600 mb-4">
          Get updates about new features and insights from the AI Navigator Profiler.
        </p>

        {!contactSubmitted ? (
          <form onSubmit={handleContactSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Email Address
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your.email@example.com"
                className="input-field"
                required
              />
            </div>
            <button
              type="submit"
              disabled={submittingContact || !email}
              className="btn-secondary flex items-center justify-center space-x-2"
            >
              {submittingContact ? (
                <>
                  <div className="w-4 h-4 border-2 border-gray-600 border-t-transparent rounded-full animate-spin"></div>
                  <span>Submitting...</span>
                </>
              ) : (
                <>
                  <Mail className="w-5 h-5" />
                  <span>Subscribe for Updates</span>
                </>
              )}
            </button>
          </form>
        ) : (
          <div className="flex items-center space-x-3 p-4 bg-green-50 rounded-lg">
            <CheckCircle className="w-6 h-6 text-green-600" />
            <div>
              <p className="text-green-800 font-medium">Thank you!</p>
              <p className="text-green-700 text-sm">
                You'll receive updates about new features and insights.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Important Notice */}
      <div className="card bg-amber-50 border-amber-200">
        <div className="flex items-start space-x-3">
          <AlertCircle className="w-6 h-6 text-amber-600 mt-0.5" />
          <div>
            <h4 className="font-semibold text-amber-800 mb-1">
              Important Notice
            </h4>
            <p className="text-amber-700 text-sm">
              This report is viewable only once. Please download your report to keep a personal copy.
              You can always return to this page to download it again.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReportViewer; 