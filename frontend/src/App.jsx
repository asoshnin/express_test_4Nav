import React, { useState } from 'react';
import LandingPage from './pages/LandingPage';
import AssessmentPage from './pages/AssessmentPage';
import ReportPage from './pages/ReportPage';

function App() {
  const [currentPage, setCurrentPage] = useState('landing');
  const [session, setSession] = useState(null);
  const [report, setReport] = useState(null);

  const handleStartAssessment = (sessionData) => {
    setSession(sessionData);
    setCurrentPage('assessment');
  };

  const handleAssessmentComplete = (reportData) => {
    setReport(reportData);
    setCurrentPage('report');
  };

  const handleRestart = () => {
    setSession(null);
    setReport(null);
    setCurrentPage('landing');
  };

  // Render the appropriate page based on current state
  switch (currentPage) {
    case 'assessment':
      return (
        <AssessmentPage
          session={session}
          onComplete={handleAssessmentComplete}
        />
      );
    case 'report':
      return (
        <ReportPage
          session={session}
          report={report}
          onRepeatAssessment={handleRestart}
        />
      );
    default:
      return (
        <LandingPage
          onStartAssessment={handleStartAssessment}
        />
      );
  }
}

export default App; 