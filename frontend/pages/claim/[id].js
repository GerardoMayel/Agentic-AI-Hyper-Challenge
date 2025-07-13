import Head from 'next/head'
import Link from 'next/link'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'

export default function ClaimDetail() {
  const router = useRouter()
  const { id } = router.query
  const [claim, setClaim] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [analyzing, setAnalyzing] = useState(false)
  const [showAnalysisModal, setShowAnalysisModal] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [actionModal, setActionModal] = useState({ show: false, action: '', title: '' })

  // Verificar autenticación
  useEffect(() => {
    const isAuthenticated = localStorage.getItem('isAuthenticated')
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    if (id) {
      fetchClaimDetails()
    }
  }, [id])

  const fetchClaimDetails = async () => {
    try {
      setLoading(true)
      const response = await fetch(`https://zurich-claims-api.onrender.com/api/analyst/claims/${id}`)
      if (!response.ok) {
        throw new Error('Failed to fetch claim details')
      }
      const data = await response.json()
      setClaim(data)
    } catch (err) {
      console.error('Error fetching claim details:', err)
      setError('Failed to load claim details')
    } finally {
      setLoading(false)
    }
  }

  const analyzeClaim = async () => {
    try {
      setAnalyzing(true)
      const response = await fetch(`https://zurich-claims-api.onrender.com/api/analyst/claims/${id}/analyze`, {
        method: 'POST'
      })
      if (!response.ok) {
        throw new Error('Failed to analyze claim')
      }
      const result = await response.json()
      setAnalysisResult(result)
      setShowAnalysisModal(true)
    } catch (err) {
      console.error('Error analyzing claim:', err)
      setError('Failed to analyze claim')
    } finally {
      setAnalyzing(false)
    }
  }

  const updateClaimStatus = async (status, reason, analystName) => {
    try {
      const response = await fetch(`https://zurich-claims-api.onrender.com/api/analyst/claims/${id}/status?status=${status}&reason=${encodeURIComponent(reason)}&analyst_name=${encodeURIComponent(analystName)}`, {
        method: 'PUT'
      })
      if (!response.ok) {
        throw new Error('Failed to update claim status')
      }
      await fetchClaimDetails() // Refresh data
      setActionModal({ show: false, action: '', title: '' })
    } catch (err) {
      console.error('Error updating claim status:', err)
      setError('Failed to update claim status')
    }
  }

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'approved': return 'bg-green-100 text-green-800'
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'rejected': return 'bg-red-100 text-red-800'
      case 'pending_information': return 'bg-orange-100 text-orange-800'
      case 'closed': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getSentimentColor = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive': return 'bg-green-500'
      case 'negative': return 'bg-red-500'
      case 'neutral': return 'bg-yellow-500'
      default: return 'bg-gray-500'
    }
  }

  const getSentimentText = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive': return 'Positive'
      case 'negative': return 'Negative'
      case 'neutral': return 'Neutral'
      default: return 'Unknown'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-blue-800 flex items-center justify-center">
        <div className="text-white text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p>Loading claim details...</p>
        </div>
      </div>
    )
  }

  if (error || !claim) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Error</h1>
          <p className="text-gray-600 mb-4">{error || 'Claim not found'}</p>
          <Link href="/dashboard" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
            Back to Dashboard
          </Link>
        </div>
      </div>
    )
  }

  return (
    <>
      <Head>
        <title>Claim {claim.claim?.claim_number} - Zurich Insurance</title>
        <meta name="description" content="Claim details and analysis" />
      </Head>

      <main className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Claim {claim.claim?.claim_number}</h1>
                <p className="text-sm text-gray-600">Customer: {claim.claim?.customer_name}</p>
              </div>
              <div className="flex items-center space-x-4">
                <button
                  onClick={analyzeClaim}
                  disabled={analyzing}
                  className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 disabled:opacity-50"
                >
                  {analyzing ? 'Analyzing...' : '🤖 AI Analysis'}
                </button>
                <Link href="/dashboard" className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700">
                  ← Back to Dashboard
                </Link>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Claim Information */}
            <div className="lg:col-span-2 space-y-6">
              {/* Claim Details Card */}
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">Claim Information</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-500">Claim Number</label>
                    <p className="text-sm text-gray-900">{claim.claim?.claim_number}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Status</label>
                    <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(claim.claim?.status)}`}>
                      {claim.claim?.status || 'New'}
                    </span>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Customer Name</label>
                    <p className="text-sm text-gray-900">{claim.claim?.customer_name}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Customer Email</label>
                    <p className="text-sm text-gray-900">{claim.claim?.customer_email}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Claim Type</label>
                    <p className="text-sm text-gray-900">{claim.claim?.claim_type}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Estimated Amount</label>
                    <p className="text-sm text-gray-900">${claim.claim?.estimated_amount || 'Not specified'}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Policy Number</label>
                    <p className="text-sm text-gray-900">{claim.claim?.policy_number || 'Not provided'}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Incident Date</label>
                    <p className="text-sm text-gray-900">
                      {claim.claim?.incident_date ? new Date(claim.claim.incident_date).toLocaleDateString() : 'Not specified'}
                    </p>
                  </div>
                </div>
              </div>

              {/* Incident Description */}
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">Incident Description</h2>
                <p className="text-sm text-gray-700 whitespace-pre-wrap">{claim.claim?.incident_description || 'No description provided'}</p>
              </div>

              {/* Email Content */}
              {claim.email && (
                <div className="bg-white shadow rounded-lg p-6">
                  <h2 className="text-lg font-medium text-gray-900 mb-4">Original Email</h2>
                  <div className="space-y-2">
                    <div>
                      <label className="text-sm font-medium text-gray-500">Subject</label>
                      <p className="text-sm text-gray-900">{claim.email.subject}</p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-500">From</label>
                      <p className="text-sm text-gray-900">{claim.email.from_email}</p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-500">Received</label>
                      <p className="text-sm text-gray-900">
                        {claim.email.received_at ? new Date(claim.email.received_at).toLocaleString() : 'Unknown'}
                      </p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-500">Content</label>
                      <div className="mt-2 p-3 bg-gray-50 rounded-md">
                        <p className="text-sm text-gray-700 whitespace-pre-wrap">{claim.email.body_text}</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Documents */}
              {claim.documents && claim.documents.length > 0 && (
                <div className="bg-white shadow rounded-lg p-6">
                  <h2 className="text-lg font-medium text-gray-900 mb-4">Documents ({claim.documents.length})</h2>
                  <div className="space-y-3">
                    {claim.documents.map((doc) => (
                      <div key={doc.id} className="flex items-center justify-between p-3 border rounded-md">
                        <div>
                          <p className="text-sm font-medium text-gray-900">{doc.original_filename}</p>
                          <p className="text-xs text-gray-500">{doc.file_type} • {(doc.file_size / 1024).toFixed(1)} KB</p>
                        </div>
                        <a
                          href={doc.storage_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-700 text-sm"
                        >
                          View
                        </a>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* AI Analysis */}
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">AI Analysis</h2>
                {claim.claim?.llm_summary ? (
                  <div className="space-y-4">
                    <div>
                      <label className="text-sm font-medium text-gray-500">Summary</label>
                      <p className="text-sm text-gray-700 mt-1">{claim.claim.llm_summary}</p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-500">Recommendation</label>
                      <span className="inline-flex px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800 mt-1">
                        {claim.claim.llm_recommendation}
                      </span>
                    </div>
                  </div>
                ) : (
                  <p className="text-sm text-gray-500">No AI analysis available</p>
                )}
              </div>

              {/* Sentiment Analysis */}
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">Customer Sentiment</h2>
                <div className="flex items-center space-x-3">
                  <div className={`w-4 h-4 rounded-full ${getSentimentColor(claim.claim?.sentiment_analysis)}`}></div>
                  <span className="text-sm text-gray-700">{getSentimentText(claim.claim?.sentiment_analysis)}</span>
                </div>
              </div>

              {/* Actions */}
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">Actions</h2>
                <div className="space-y-3">
                  <button
                    onClick={() => setActionModal({ show: true, action: 'APPROVED', title: 'Approve Claim' })}
                    className="w-full bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
                  >
                    ✅ Approve Claim
                  </button>
                  <button
                    onClick={() => setActionModal({ show: true, action: 'REJECTED', title: 'Reject Claim' })}
                    className="w-full bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700"
                  >
                    ❌ Reject Claim
                  </button>
                  <button
                    onClick={() => setActionModal({ show: true, action: 'PENDING_INFORMATION', title: 'Request More Information' })}
                    className="w-full bg-yellow-600 text-white px-4 py-2 rounded-md hover:bg-yellow-700"
                  >
                    📋 Request More Info
                  </button>
                  <button
                    onClick={() => setActionModal({ show: true, action: 'CLOSED', title: 'Close Claim' })}
                    className="w-full bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700"
                  >
                    🔒 Close Claim
                  </button>
                </div>
              </div>

              {/* Status History */}
              {claim.status_updates && claim.status_updates.length > 0 && (
                <div className="bg-white shadow rounded-lg p-6">
                  <h2 className="text-lg font-medium text-gray-900 mb-4">Status History</h2>
                  <div className="space-y-3">
                    {claim.status_updates.map((update) => (
                      <div key={update.id} className="border-l-4 border-blue-500 pl-3">
                        <p className="text-sm font-medium text-gray-900">
                          {update.old_status} → {update.new_status}
                        </p>
                        <p className="text-xs text-gray-500">
                          {new Date(update.created_at).toLocaleString()}
                        </p>
                        {update.reason && (
                          <p className="text-xs text-gray-600 mt-1">{update.reason}</p>
                        )}
                        {update.analyst_name && (
                          <p className="text-xs text-gray-500">by {update.analyst_name}</p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Analysis Modal */}
        {showAnalysisModal && analysisResult && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-screen overflow-y-auto">
              <div className="px-6 py-4 border-b border-gray-200">
                <div className="flex justify-between items-center">
                  <h3 className="text-lg font-medium text-gray-900">AI Analysis Result</h3>
                  <button onClick={() => setShowAnalysisModal(false)} className="text-gray-400 hover:text-gray-600">
                    ✕
                  </button>
                </div>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-gray-500">Summary</label>
                    <p className="text-sm text-gray-700 mt-1">{analysisResult.summary}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Risk Assessment</label>
                    <p className="text-sm text-gray-700 mt-1">{analysisResult.risk_assessment}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Document Analysis</label>
                    <p className="text-sm text-gray-700 mt-1">{analysisResult.document_analysis}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Recommendation</label>
                    <span className="inline-flex px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800 mt-1">
                      {analysisResult.recommendation}
                    </span>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Reason for Closure</label>
                    <p className="text-sm text-gray-700 mt-1">{analysisResult.reason_for_closure}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Suggested Amount</label>
                    <p className="text-sm text-gray-700 mt-1">${analysisResult.suggested_amount}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Priority</label>
                    <span className="inline-flex px-2 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-800 mt-1">
                      {analysisResult.priority}
                    </span>
                  </div>
                </div>
                <div className="flex justify-end space-x-3 mt-6">
                  <button
                    onClick={() => setShowAnalysisModal(false)}
                    className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                  >
                    Close
                  </button>
                  <button
                    onClick={() => {
                      setShowAnalysisModal(false)
                      setActionModal({ 
                        show: true, 
                        action: analysisResult.recommendation === 'APPROVE' ? 'APPROVED' : 
                               analysisResult.recommendation === 'REJECT' ? 'REJECTED' : 'PENDING_INFORMATION',
                        title: `Apply AI Recommendation: ${analysisResult.recommendation}`
                      })
                    }}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                  >
                    Apply Recommendation
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Action Modal */}
        {actionModal.show && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">{actionModal.title}</h3>
              </div>
              <div className="p-6">
                <form onSubmit={(e) => {
                  e.preventDefault()
                  const formData = new FormData(e.target)
                  updateClaimStatus(
                    actionModal.action,
                    formData.get('reason'),
                    formData.get('analyst_name')
                  )
                }}>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Analyst Name</label>
                      <input
                        type="text"
                        name="analyst_name"
                        required
                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        placeholder="Enter your name"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Reason</label>
                      <textarea
                        name="reason"
                        required
                        rows={3}
                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        placeholder="Enter the reason for this action"
                      />
                    </div>
                  </div>
                  <div className="flex justify-end space-x-3 mt-6">
                    <button
                      type="button"
                      onClick={() => setActionModal({ show: false, action: '', title: '' })}
                      className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                    >
                      Submit
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        )}
      </main>
    </>
  )
} 