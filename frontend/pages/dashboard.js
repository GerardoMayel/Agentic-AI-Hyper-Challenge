import Head from 'next/head'
import Link from 'next/link'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'

export default function Dashboard() {
  const router = useRouter()
  const [stats, setStats] = useState({
    claims_summary: {
      total_claims: 0,
      pending_claims: 0,
      approved_claims: 0,
      rejected_claims: 0,
      closed_claims: 0
    },
    processing_summary: {
      total_emails: 0,
      processed_emails: 0,
      unprocessed_emails: 0,
      total_documents: 0
    },
    financial_summary: {
      total_amount_requested: 0,
      total_amount_approved: 0,
      approval_rate: 0
    }
  })
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

  const fetchData = async (retryCount = 0) => {
    const maxRetries = 3
    const baseDelay = 2000 // 2 seconds base delay
    
    try {
      setLoading(true)
      setError('')
      
      console.log(`🔄 Attempting to fetch dashboard data (attempt ${retryCount + 1}/${maxRetries + 1})`)
      
      // Fetch stats with timeout
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 15000) // 15 second timeout
      
      const statsResponse = await fetch('https://zurich-claims-api.onrender.com/api/analyst/dashboard/stats', {
        signal: controller.signal
      })
      
      clearTimeout(timeoutId)
      
      if (!statsResponse.ok) {
        throw new Error(`HTTP ${statsResponse.status}: ${statsResponse.statusText}`)
      }
      
      const statsData = await statsResponse.json()
      console.log('✅ Dashboard data loaded successfully:', statsData)
      setStats(statsData)
      
    } catch (err) {
      console.error(`❌ Error fetching data (attempt ${retryCount + 1}):`, err)
      
      if (retryCount < maxRetries) {
        const delay = baseDelay * Math.pow(2, retryCount) // Exponential backoff
        console.log(`⏳ Retrying in ${delay/1000} seconds...`)
        
        setError(`Database connection slow, retrying... (${retryCount + 1}/${maxRetries + 1})`)
        
        setTimeout(() => {
          fetchData(retryCount + 1)
        }, delay)
        return
      } else {
        setError(`Failed to load dashboard data after ${maxRetries + 1} attempts. The database may be temporarily unavailable.`)
      }
    } finally {
      if (retryCount >= maxRetries) {
        setLoading(false)
      }
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
          <p className="text-lg mb-2">Loading dashboard data...</p>
          <p className="text-sm text-blue-200">Connecting to database (this may take a few seconds)</p>
          {error && (
            <div className="mt-4 p-3 bg-yellow-900/50 rounded-lg">
              <p className="text-yellow-200 text-sm">{error}</p>
            </div>
          )}
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
              <div className="flex items-center">
                <div className="text-red-500 mr-3">⚠️</div>
                <div>
                  <p className="text-red-600 font-medium">{error}</p>
                  <button 
                    onClick={() => fetchData()}
                    className="mt-2 text-red-700 underline hover:no-underline"
                  >
                    Try again
                  </button>
                </div>
              </div>
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
                <div className="text-4xl font-bold text-blue-600 mb-2">{stats.claims_summary?.total_claims || 0}</div>
                <p className="text-slate-600 font-medium">All time</p>
              </div>
              
              <div className="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 text-center">
                <div className="text-5xl mb-4">⏳</div>
                <h3 className="text-2xl font-bold text-slate-800 mb-2">Pending</h3>
                <div className="text-4xl font-bold text-orange-600 mb-2">{stats.claims_summary?.pending_claims || 0}</div>
                <p className="text-slate-600 font-medium">Under review</p>
              </div>
              
              <div className="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 text-center">
                <div className="text-5xl mb-4">✅</div>
                <h3 className="text-2xl font-bold text-slate-800 mb-2">Approved</h3>
                <div className="text-4xl font-bold text-green-600 mb-2">{stats.claims_summary?.approved_claims || 0}</div>
                <p className="text-slate-600 font-medium">Processed</p>
              </div>
              
              <div className="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 text-center">
                <div className="text-5xl mb-4">❌</div>
                <h3 className="text-2xl font-bold text-slate-800 mb-2">Rejected</h3>
                <div className="text-4xl font-bold text-red-600 mb-2">{stats.claims_summary?.rejected_claims || 0}</div>
                <p className="text-slate-600 font-medium">Declined</p>
              </div>
              
              <div className="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 text-center">
                <div className="text-5xl mb-4">📧</div>
                <h3 className="text-2xl font-bold text-slate-800 mb-2">Total Emails</h3>
                <div className="text-4xl font-bold text-purple-600 mb-2">{stats.processing_summary?.total_emails || 0}</div>
                <p className="text-slate-600 font-medium">Received</p>
              </div>
              
              <div className="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 text-center">
                <div className="text-5xl mb-4">⚡</div>
                <h3 className="text-2xl font-bold text-slate-800 mb-2">Processed</h3>
                <div className="text-4xl font-bold text-indigo-600 mb-2">{stats.processing_summary?.processed_emails || 0}</div>
                <p className="text-slate-600 font-medium">Automated</p>
              </div>
            </div>
          </div>
        </div>

        {/* Analyst Access Section */}
        <div className="w-full py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-slate-800 text-center mb-12">
              Analyst Access
            </h2>
            <div className="bg-white rounded-xl shadow-lg border border-slate-100 p-8 text-center">
              <div className="text-6xl mb-6">🔍</div>
              <h3 className="text-2xl font-bold text-slate-800 mb-4">
                Detailed Claims Analysis
              </h3>
              <p className="text-slate-600 mb-8 max-w-2xl mx-auto">
                Access the comprehensive analyst interface to review individual claims, 
                view AI recommendations, and make final determinations on claim status.
              </p>
              <a 
                href="https://zurich-claims-api.onrender.com/analyst"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-blue-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:bg-blue-700 transition-all duration-300 transform hover:scale-105 shadow-xl"
              >
                Open Analyst Interface
              </a>
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