import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://zurich-claims-api.onrender.com';

export default function AnalystDashboard() {
  const [stats, setStats] = useState(null);
  const [claims, setClaims] = useState([]);
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedClaim, setSelectedClaim] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [sentimentAnalysis, setSentimentAnalysis] = useState(null);
  const [claimDocuments, setClaimDocuments] = useState([]);
  const [showDocuments, setShowDocuments] = useState(false);
  const [showSentiment, setShowSentiment] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Load stats with retry logic
      const statsResponse = await fetchWithRetry(`${API_BASE_URL}/api/analyst/dashboard/stats`);
      const statsData = await statsResponse.json();
      setStats(statsData);

      // Load claims with retry logic
      const claimsResponse = await fetchWithRetry(`${API_BASE_URL}/api/analyst/claims`);
      const claimsData = await claimsResponse.json();
      setClaims(claimsData);

      // Load recent emails with retry logic
      const emailsResponse = await fetchWithRetry(`${API_BASE_URL}/api/analyst/emails?limit=5`);
      const emailsData = await emailsResponse.json();
      setEmails(emailsData);

    } catch (err) {
      setError('Failed to load dashboard data. Please try again.');
      console.error('Dashboard load error:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchWithRetry = async (url, maxRetries = 3) => {
    for (let i = 0; i < maxRetries; i++) {
      try {
        const response = await fetch(url);
        if (response.ok) {
          return response;
        }
      } catch (err) {
        if (i === maxRetries - 1) throw err;
        await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, i)));
      }
    }
    throw new Error('Request failed after retries');
  };

  const analyzeClaim = async (claimId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/analyst/claims/${claimId}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const result = await response.json();
        setAnalysisResult(result);
        setSelectedClaim(claimId);
      } else {
        setError('Failed to analyze claim');
      }
    } catch (err) {
      setError('Error analyzing claim');
      console.error('Analysis error:', err);
    }
  };

  const updateClaimStatus = async (claimId, status, reason) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/analyst/claims/${claimId}/status?status=${status}&reason=${encodeURIComponent(reason)}&analyst_name=AI Test Analyst`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        // Reload data to show updated status
        loadDashboardData();
        setAnalysisResult(null);
        setSelectedClaim(null);
      } else {
        setError('Failed to update claim status');
      }
    } catch (err) {
      setError('Error updating claim status');
      console.error('Status update error:', err);
    }
  };

  const analyzeSentiment = async (claimId) => {
    try {
      setSentimentAnalysis(null);
      const response = await fetch(`${API_BASE_URL}/api/analyst/claims/${claimId}/sentiment-analysis`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const result = await response.json();
        setSentimentAnalysis(result);
        setShowSentiment(true);
        setShowDocuments(false);
      } else {
        setError('Failed to analyze sentiment');
      }
    } catch (err) {
      setError('Error analyzing sentiment');
      console.error('Sentiment analysis error:', err);
    }
  };

  const loadClaimDocuments = async (claimId) => {
    try {
      setClaimDocuments([]);
      const response = await fetch(`${API_BASE_URL}/api/analyst/claims/${claimId}/documents`);
      
      if (response.ok) {
        const result = await response.json();
        setClaimDocuments(result.documents || []);
        setShowDocuments(true);
        setShowSentiment(false);
      } else {
        setError('Failed to load documents');
      }
    } catch (err) {
      setError('Error loading documents');
      console.error('Documents load error:', err);
    }
  };

  const getTrafficLightColor = (trafficLight) => {
    switch (trafficLight) {
      case 'red': return 'bg-red-500';
      case 'yellow': return 'bg-yellow-500';
      case 'green': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'urgent': return 'bg-red-100 text-red-800';
      case 'high': return 'bg-orange-100 text-orange-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
              <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading analyst interface...</p>
        <p className="text-sm text-gray-500">Connecting to claims database</p>
      </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Analyst Dashboard - Claims Management</title>
        <meta name="description" content="Analyst dashboard for claims management" />
      </Head>

      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">Analyst Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/dashboard" className="text-blue-600 hover:text-blue-800">
                ← Back to Dashboard
              </Link>
              <button
                onClick={loadDashboardData}
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
              >
                Refresh
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Error Message */}
      {error && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-4">
          <div className="bg-red-50 border border-red-200 rounded-md p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Total Claims</p>
                  <p className="text-2xl font-semibold text-gray-900">{stats.total_claims || 0}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Pending</p>
                  <p className="text-2xl font-semibold text-gray-900">{stats.pending_claims || 0}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Approved</p>
                  <p className="text-2xl font-semibold text-gray-900">{stats.approved_claims || 0}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-red-500 rounded-md flex items-center justify-center">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Rejected</p>
                  <p className="text-2xl font-semibold text-gray-900">{stats.rejected_claims || 0}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Claims List */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">Recent Claims</h2>
            </div>
            <div className="divide-y divide-gray-200">
              {claims.length > 0 ? (
                claims.map((claim) => (
                  <div key={claim.id} className="px-6 py-4">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <h3 className="text-sm font-medium text-gray-900">{claim.claim_number}</h3>
                        <p className="text-sm text-gray-500">{claim.customer_name}</p>
                        <p className="text-xs text-gray-400">{claim.claim_type}</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          claim.status === 'PENDING' ? 'bg-yellow-100 text-yellow-800' :
                          claim.status === 'APPROVED' ? 'bg-green-100 text-green-800' :
                          claim.status === 'REJECTED' ? 'bg-red-100 text-red-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {claim.status}
                        </span>
                        <button
                          onClick={() => analyzeClaim(claim.id)}
                          className="text-blue-600 hover:text-blue-800 text-sm"
                        >
                          Analyze
                        </button>
                        <button
                          onClick={() => analyzeSentiment(claim.id)}
                          className="text-purple-600 hover:text-purple-800 text-sm"
                        >
                          Sentiment
                        </button>
                        <button
                          onClick={() => loadClaimDocuments(claim.id)}
                          className="text-green-600 hover:text-green-800 text-sm"
                        >
                          Documents
                        </button>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="px-6 py-4 text-center text-gray-500">
                  No claims found
                </div>
              )}
            </div>
          </div>

          {/* Recent Emails */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">Recent Emails</h2>
            </div>
            <div className="divide-y divide-gray-200">
              {emails.length > 0 ? (
                emails.map((email) => (
                  <div key={email.id} className="px-6 py-4">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <h3 className="text-sm font-medium text-gray-900">{email.subject}</h3>
                        <p className="text-sm text-gray-500">{email.sender}</p>
                        <p className="text-xs text-gray-400">{new Date(email.received_at).toLocaleDateString()}</p>
                      </div>
                      <div className="flex items-center">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          email.is_processed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {email.is_processed ? 'Processed' : 'Pending'}
                        </span>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="px-6 py-4 text-center text-gray-500">
                  No emails found
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Analysis Result */}
        {analysisResult && selectedClaim && (
          <div className="mt-8 bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">AI Analysis Result</h2>
            </div>
            <div className="px-6 py-4">
              <div className="mb-4">
                <h3 className="text-sm font-medium text-gray-900 mb-2">Summary</h3>
                <p className="text-sm text-gray-600">{analysisResult.summary}</p>
              </div>
              <div className="mb-4">
                <h3 className="text-sm font-medium text-gray-900 mb-2">Recommendation</h3>
                <p className="text-sm text-gray-600">{analysisResult.recommendation}</p>
              </div>
              <div className="flex space-x-4">
                <button
                  onClick={() => updateClaimStatus(selectedClaim, 'APPROVED', 'AI recommendation: APPROVE')}
                  className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
                >
                  Approve
                </button>
                <button
                  onClick={() => updateClaimStatus(selectedClaim, 'REJECTED', 'AI recommendation: REJECT')}
                  className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700"
                >
                  Reject
                </button>
                <button
                  onClick={() => updateClaimStatus(selectedClaim, 'PENDING_INFORMATION', 'AI recommendation: REQUEST_MORE_DOCS')}
                  className="bg-yellow-600 text-white px-4 py-2 rounded-md hover:bg-yellow-700"
                >
                  Request More Info
                </button>
                <button
                  onClick={() => {
                    setAnalysisResult(null);
                    setSelectedClaim(null);
                  }}
                  className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Sentiment Analysis Result */}
        {sentimentAnalysis && showSentiment && (
          <div className="mt-8 bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">AI Sentiment Analysis</h2>
            </div>
            <div className="px-6 py-4">
              {sentimentAnalysis.analysis && (
                <div className="space-y-6">
                  {/* Traffic Light */}
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-2">
                      <span className="text-sm font-medium text-gray-700">Risk Level:</span>
                      <div className={`w-4 h-4 rounded-full ${getTrafficLightColor(sentimentAnalysis.analysis.traffic_light)}`}></div>
                      <span className="text-sm text-gray-600 capitalize">{sentimentAnalysis.analysis.traffic_light}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm font-medium text-gray-700">Priority:</span>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityColor(sentimentAnalysis.analysis.priority_level)}`}>
                        {sentimentAnalysis.analysis.priority_level}
                      </span>
                    </div>
                  </div>

                  {/* Scores */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Sentiment Score</h4>
                      <div className="flex items-center">
                        <div className="flex-1 bg-gray-200 rounded-full h-2 mr-2">
                          <div 
                            className="bg-blue-600 h-2 rounded-full" 
                            style={{ width: `${(sentimentAnalysis.analysis.sentiment_score || 0) * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-sm text-gray-600">{(sentimentAnalysis.analysis.sentiment_score || 0) * 100}%</span>
                      </div>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Risk Score</h4>
                      <div className="flex items-center">
                        <div className="flex-1 bg-gray-200 rounded-full h-2 mr-2">
                          <div 
                            className="bg-red-600 h-2 rounded-full" 
                            style={{ width: `${(sentimentAnalysis.analysis.risk_score || 0) * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-sm text-gray-600">{(sentimentAnalysis.analysis.risk_score || 0) * 100}%</span>
                      </div>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="text-sm font-medium text-gray-700 mb-2">AI Confidence</h4>
                      <div className="flex items-center">
                        <div className="flex-1 bg-gray-200 rounded-full h-2 mr-2">
                          <div 
                            className="bg-green-600 h-2 rounded-full" 
                            style={{ width: `${(sentimentAnalysis.analysis.ai_confidence || 0) * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-sm text-gray-600">{(sentimentAnalysis.analysis.ai_confidence || 0) * 100}%</span>
                      </div>
                    </div>
                  </div>

                  {/* Analysis Details */}
                  <div className="space-y-4">
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Sentiment Analysis</h4>
                      <p className="text-sm text-gray-600">{sentimentAnalysis.analysis.sentiment_analysis}</p>
                    </div>
                    
                    {sentimentAnalysis.analysis.risk_factors && sentimentAnalysis.analysis.risk_factors.length > 0 && (
                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-2">Risk Factors</h4>
                        <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                          {sentimentAnalysis.analysis.risk_factors.map((factor, index) => (
                            <li key={index}>{factor}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {sentimentAnalysis.analysis.recommendations && (
                      <div className="space-y-3">
                        <h4 className="text-sm font-medium text-gray-700">AI Recommendations</h4>
                        
                        {sentimentAnalysis.analysis.recommendations.immediate_actions && (
                          <div>
                            <h5 className="text-xs font-medium text-gray-600 mb-1">Immediate Actions</h5>
                            <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                              {sentimentAnalysis.analysis.recommendations.immediate_actions.map((action, index) => (
                                <li key={index}>{action}</li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {sentimentAnalysis.analysis.recommendations.investigation_steps && (
                          <div>
                            <h5 className="text-xs font-medium text-gray-600 mb-1">Investigation Steps</h5>
                            <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                              {sentimentAnalysis.analysis.recommendations.investigation_steps.map((step, index) => (
                                <li key={index}>{step}</li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {sentimentAnalysis.analysis.recommendations.documentation_needed && (
                          <div>
                            <h5 className="text-xs font-medium text-gray-600 mb-1">Required Documentation</h5>
                            <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                              {sentimentAnalysis.analysis.recommendations.documentation_needed.map((doc, index) => (
                                <li key={index}>{doc}</li>
                              ))}
                            </ul>
                          </div>
                        )}

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div>
                            <h5 className="text-xs font-medium text-gray-600 mb-1">Communication Strategy</h5>
                            <p className="text-sm text-gray-600">{sentimentAnalysis.analysis.recommendations.communication_strategy}</p>
                          </div>
                          <div>
                            <h5 className="text-xs font-medium text-gray-600 mb-1">Processing Time</h5>
                            <p className="text-sm text-gray-600">{sentimentAnalysis.analysis.recommendations.estimated_processing_time}</p>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="flex justify-end">
                    <button
                      onClick={() => {
                        setSentimentAnalysis(null);
                        setShowSentiment(false);
                      }}
                      className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700"
                    >
                      Close
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Documents List */}
        {showDocuments && claimDocuments.length > 0 && (
          <div className="mt-8 bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">Claim Documents ({claimDocuments.length})</h2>
            </div>
            <div className="px-6 py-4">
              <div className="space-y-4">
                {claimDocuments.map((doc) => (
                  <div key={doc.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                          <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                        </div>
                        <div>
                          <h4 className="text-sm font-medium text-gray-900">{doc.original_filename}</h4>
                          <p className="text-xs text-gray-500">{doc.document_type} • {(doc.file_size / 1024).toFixed(1)} KB</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          doc.is_processed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {doc.is_processed ? 'Processed' : 'Pending'}
                        </span>
                        {doc.inferred_costs && (
                          <span className="text-xs text-gray-600">Cost: {doc.inferred_costs}</span>
                        )}
                      </div>
                    </div>
                    
                    {doc.ocr_text && (
                      <div className="mt-3">
                        <h5 className="text-xs font-medium text-gray-700 mb-2">Extracted Text</h5>
                        <div className="bg-gray-50 p-3 rounded text-sm text-gray-600 max-h-32 overflow-y-auto">
                          {doc.ocr_text}
                        </div>
                      </div>
                    )}

                    {doc.structured_data && Object.keys(doc.structured_data).length > 0 && (
                      <div className="mt-3">
                        <h5 className="text-xs font-medium text-gray-700 mb-2">Structured Data</h5>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                          {Object.entries(doc.structured_data).map(([key, values]) => (
                            <div key={key} className="bg-gray-50 p-2 rounded">
                              <span className="font-medium text-gray-700">{key}:</span>
                              <div className="text-gray-600">
                                {Array.isArray(values) ? values.slice(0, 2).join(', ') : values}
                                {Array.isArray(values) && values.length > 2 && ` (+${values.length - 2} more)`}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
              
              <div className="flex justify-end mt-4">
                <button
                  onClick={() => {
                    setShowDocuments(false);
                    setClaimDocuments([]);
                  }}
                  className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 