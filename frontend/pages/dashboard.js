import Head from 'next/head'
import Link from 'next/link'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'

export default function Dashboard() {
  const router = useRouter()
  const [stats, setStats] = useState({
    total_claims: 0,
    pending_claims: 0,
    approved_claims: 0,
    rejected_claims: 0,
    total_emails: 0,
    processed_emails: 0
  })
  const [claims, setClaims] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // Verificar autenticación
  useEffect(() => {
    const isAuthenticated = localStorage.getItem('isAuthenticated')
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      
      // Fetch stats
      const statsResponse = await fetch('https://zurich-claims-api.onrender.com/api/analyst/dashboard/stats')
      const statsData = await statsResponse.json()
      setStats(statsData)

      // Fetch claims
      const claimsResponse = await fetch('https://zurich-claims-api.onrender.com/api/analyst/claims')
      const claimsData = await claimsResponse.json()
      setClaims(claimsData)
      
    } catch (err) {
      console.error('Error fetching data:', err)
      setError('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'approved': return 'bg-green-100 text-green-800'
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'rejected': return 'bg-red-100 text-red-800'
      case 'pending_information': return 'bg-orange-100 text-orange-800'
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

  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('userEmail')
    router.push('/login')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-blue-800 flex items-center justify-center">
        <div className="text-white text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p>Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <>
      <Head>
        <title>Dashboard - Zurich Insurance</title>
        <meta name="description" content="Claims dashboard" />
      </Head>

      <main className="min-h-screen">
        {/* Header */}
        <div className="w-full py-16 bg-gradient-to-br from-slate-900 via-blue-900 to-blue-800 shadow-2xl">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex justify-between items-center">
              <div className="text-center flex-1">
                <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
                  Claims Dashboard
                </h1>
                <p className="text-xl text-blue-100">Monitor and manage insurance claims</p>
              </div>
              <button
                onClick={handleLogout}
                className="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>

        {error && (
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-600">{error}</p>
            </div>
          </div>
        )}

        {/* Stats Section */}
        <div className="w-full py-16 bg-gradient-to-br from-slate-50 to-blue-50">
          <div className="max-w-7xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-slate-800 text-center mb-12">
              System Overview
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              <div className="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 text-center">
                <div className="text-5xl mb-4">📊</div>
                <h3 className="text-2xl font-bold text-slate-800 mb-2">Total Claims</h3>
                <div className="text-4xl font-bold text-blue-600 mb-2">{stats.total_claims}</div>
                <p className="text-slate-600 font-medium">All time</p>
              </div>
              
              <div className="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 text-center">
                <div className="text-5xl mb-4">⏳</div>
                <h3 className="text-2xl font-bold text-slate-800 mb-2">Pending</h3>
                <div className="text-4xl font-bold text-orange-600 mb-2">{stats.pending_claims}</div>
                <p className="text-slate-600 font-medium">Under review</p>
              </div>
              
              <div className="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 text-center">
                <div className="text-5xl mb-4">✅</div>
                <h3 className="text-2xl font-bold text-slate-800 mb-2">Approved</h3>
                <div className="text-4xl font-bold text-green-600 mb-2">{stats.approved_claims}</div>
                <p className="text-slate-600 font-medium">Processed</p>
              </div>
              
              <div className="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 text-center">
                <div className="text-5xl mb-4">❌</div>
                <h3 className="text-2xl font-bold text-slate-800 mb-2">Rejected</h3>
                <div className="text-4xl font-bold text-red-600 mb-2">{stats.rejected_claims}</div>
                <p className="text-slate-600 font-medium">Declined</p>
              </div>
              
              <div className="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 text-center">
                <div className="text-5xl mb-4">📧</div>
                <h3 className="text-2xl font-bold text-slate-800 mb-2">Total Emails</h3>
                <div className="text-4xl font-bold text-purple-600 mb-2">{stats.total_emails}</div>
                <p className="text-slate-600 font-medium">Received</p>
              </div>
              
              <div className="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 text-center">
                <div className="text-5xl mb-4">⚡</div>
                <h3 className="text-2xl font-bold text-slate-800 mb-2">Processed</h3>
                <div className="text-4xl font-bold text-indigo-600 mb-2">{stats.processed_emails}</div>
                <p className="text-slate-600 font-medium">Automated</p>
              </div>
            </div>
          </div>
        </div>

        {/* Claims Table */}
        <div className="w-full py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-slate-800 text-center mb-12">
              Recent Claims
            </h2>
            <div className="bg-white rounded-xl shadow-lg border border-slate-100 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-slate-50">
                    <tr>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700">Claim ID</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700">Customer Email</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700">Status</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700">Sentiment</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700">Created</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {claims.map((claim) => (
                      <tr key={claim.id} className="hover:bg-slate-50">
                        <td className="px-6 py-4 text-sm font-medium text-slate-900">{claim.claim_id}</td>
                        <td className="px-6 py-4 text-sm text-slate-700">{claim.customer_email}</td>
                        <td className="px-6 py-4">
                          <span className={`px-3 py-1 text-xs font-medium rounded-full ${getStatusColor(claim.status)}`}>
                            {claim.status || 'New'}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center space-x-2">
                            <div className={`w-3 h-3 rounded-full ${getSentimentColor(claim.sentiment_analysis)}`}></div>
                            <span className="text-sm text-slate-700">{getSentimentText(claim.sentiment_analysis)}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-slate-700">
                          {new Date(claim.created_at).toLocaleDateString()}
                        </td>
                        <td className="px-6 py-4">
                          <Link 
                            href={`/claim/${claim.id}`}
                            className="text-blue-600 hover:text-blue-700 text-sm font-medium"
                          >
                            View Details
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        {/* Back Link */}
        <div className="w-full py-12 bg-slate-50">
          <div className="max-w-4xl mx-auto px-4 text-center">
            <Link 
              href="/"
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
            >
              ← Back to Home
            </Link>
          </div>
        </div>
      </main>
    </>
  )
} 