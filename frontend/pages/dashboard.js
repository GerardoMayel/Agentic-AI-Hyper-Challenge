import Head from 'next/head'
import Link from 'next/link'

export default function Dashboard() {
  // Datos mock para el dashboard
  const stats = [
    { label: 'Total Claims', value: '1,247', change: '+12%', color: 'text-blue-600' },
    { label: 'Pending', value: '89', change: 'Under review', color: 'text-orange-600' },
    { label: 'Approved', value: '1,158', change: '92.9% approval rate', color: 'text-green-600' }
  ]

  const recentClaims = [
    { id: 'CLM-001', name: 'John Doe', type: 'Trip Cancellation', status: 'pending', date: '2024-01-15' },
    { id: 'CLM-002', name: 'Jane Smith', type: 'Trip Delay', status: 'approved', date: '2024-01-14' },
    { id: 'CLM-003', name: 'Bob Johnson', type: 'Baggage Delay', status: 'rejected', date: '2024-01-13' }
  ]

  const getStatusColor = (status) => {
    switch (status) {
      case 'approved': return 'bg-green-100 text-green-800'
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'rejected': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
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
          <div className="max-w-4xl mx-auto px-4 text-center">
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Claims Dashboard
            </h1>
            <p className="text-xl text-blue-100">Monitor and manage insurance claims</p>
          </div>
        </div>

        {/* Stats Section */}
        <div className="w-full py-16 bg-gradient-to-br from-slate-50 to-blue-50">
          <div className="max-w-7xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-slate-800 text-center mb-12">
              System Overview
            </h2>
            <div className="flex gap-8 flex-wrap">
              {stats.map((stat, index) => (
                <div key={index} className="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 flex-1 text-center">
                  <div className="text-5xl mb-4">📊</div>
                  <h3 className="text-2xl font-bold text-slate-800 mb-2">{stat.label}</h3>
                  <div className={`text-4xl font-bold mb-2 ${stat.color}`}>{stat.value}</div>
                  <p className="text-slate-600 font-medium">{stat.change}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recent Claims */}
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
                      <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700">Customer</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700">Type</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700">Status</th>
                      <th className="px-6 py-4 text-left text-sm font-semibold text-slate-700">Date</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {recentClaims.map((claim) => (
                      <tr key={claim.id} className="hover:bg-slate-50">
                        <td className="px-6 py-4 text-sm font-medium text-slate-900">{claim.id}</td>
                        <td className="px-6 py-4 text-sm text-slate-700">{claim.name}</td>
                        <td className="px-6 py-4 text-sm text-slate-700">{claim.type}</td>
                        <td className="px-6 py-4">
                          <span className={`px-3 py-1 text-xs font-medium rounded-full ${getStatusColor(claim.status)}`}>
                            {claim.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-slate-700">{claim.date}</td>
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