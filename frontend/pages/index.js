import Head from 'next/head'
import Link from 'next/link'

export default function Home() {
  return (
    <>
      <Head>
        <title>Zurich Insurance - Claims Management System</title>
        <meta name="description" content="Professional insurance claims management system" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen">
        {/* Hero Section */}
        <div className="w-full py-20 bg-gradient-to-br from-slate-900 via-blue-900 to-blue-800 shadow-2xl relative overflow-hidden">
          <div className="max-w-6xl mx-auto px-4">
            <div className="text-center">
              <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 tracking-tight">
                🏢 Zurich Insurance
              </h1>
              <h2 className="text-3xl md:text-4xl font-semibold text-blue-100 mb-8">
                Claims Management System
              </h2>
              <p className="text-xl text-blue-200 max-w-3xl mx-auto mb-12 leading-relaxed">
                Professional insurance claims management system with advanced automation
              </p>
              <div className="w-32 h-px bg-blue-300 mx-auto my-8"></div>
              <div className="flex gap-4 flex-wrap justify-center">
                <Link 
                  href="/claim-form"
                  className="bg-white text-slate-800 px-8 py-4 rounded-2xl font-bold text-lg hover:bg-blue-50 transition-all duration-300 transform hover:scale-105 shadow-2xl"
                >
                  📝 Submit Claim
                </Link>
                <Link 
                  href="/dashboard"
                  className="border-2 border-white text-white px-8 py-4 rounded-2xl font-bold text-lg hover:bg-white hover:text-slate-800 transition-all duration-300 transform hover:scale-105"
                >
                  📊 View Dashboard
                </Link>
                <Link 
                  href="/login"
                  className="border-2 border-white text-white px-8 py-4 rounded-2xl font-bold text-lg hover:bg-white hover:text-slate-800 transition-all duration-300 transform hover:scale-105"
                >
                  🔐 Analyst Login
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="w-full py-16 bg-gradient-to-br from-slate-50 to-blue-50">
          <div className="max-w-6xl mx-auto px-4">
            <h2 className="text-4xl font-bold text-slate-800 text-center mb-12">
              Key Features
            </h2>
            <div className="flex gap-6 flex-wrap">
              <div className="p-6 bg-white rounded-xl shadow-lg border border-slate-100 flex-1 text-center">
                <div className="text-5xl mb-4">🚀</div>
                <h3 className="text-xl font-bold text-slate-800 mb-3">Fast Processing</h3>
                <p className="text-slate-600 text-sm">
                  Automated AI-powered analysis for faster response times.
                </p>
              </div>
              <div className="p-6 bg-white rounded-xl shadow-lg border border-slate-100 flex-1 text-center">
                <div className="text-5xl mb-4">🔒</div>
                <h3 className="text-xl font-bold text-slate-800 mb-3">Secure & Reliable</h3>
                <p className="text-slate-600 text-sm">
                  Enterprise-grade security with encrypted data storage.
                </p>
              </div>
              <div className="p-6 bg-white rounded-xl shadow-lg border border-slate-100 flex-1 text-center">
                <div className="text-5xl mb-4">📱</div>
                <h3 className="text-xl font-bold text-slate-800 mb-3">Multi-Platform</h3>
                <p className="text-slate-600 text-sm">
                  Responsive design that works on all devices.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="w-full py-16 bg-white">
          <div className="max-w-4xl mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold text-slate-800 mb-6">
              Ready to Get Started?
            </h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto mb-8">
              Access our professional claims management system
            </p>
            <div className="flex gap-4 flex-wrap justify-center">
              <Link 
                href="/claim-form"
                className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-8 py-4 rounded-xl font-bold text-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-300 transform hover:scale-105 shadow-xl"
              >
                📝 Submit Claim
              </Link>
              <Link 
                href="/dashboard"
                className="border-2 border-blue-600 text-blue-600 px-8 py-4 rounded-xl font-bold text-lg hover:bg-blue-600 hover:text-white transition-all duration-300 transform hover:scale-105"
              >
                📊 View Dashboard
              </Link>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="w-full py-12 bg-slate-50 border-t border-slate-200">
          <div className="max-w-4xl mx-auto px-4 text-center">
            <p className="text-slate-500">© 2024 Zurich Insurance. All rights reserved.</p>
            <p className="text-slate-400 text-sm">Professional insurance solutions for a secure future</p>
          </div>
        </div>
      </main>
    </>
  )
} 