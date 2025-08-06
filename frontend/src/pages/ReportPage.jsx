import React from 'react';
import Header from '../components/common/Header';
import ReportViewer from '../components/assessment/ReportViewer';

const ReportPage = ({ session, report }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header currentPage="report" nickname={session?.nickname} />
      
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <ReportViewer
          report={report}
          sessionId={session?.sessionId}
        />
      </div>
    </div>
  );
};

export default ReportPage; 