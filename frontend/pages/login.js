import Head from 'next/head'
import Link from 'next/link'
import { useState } from 'react'
import { useRouter } from 'next/router'

export default function Login() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  // Credenciales simples para demo
  const VALID_CREDENTIALS = {
    email: 'analyst@zurich.com',
    password: 'zurich2024'
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    // Simular delay de autenticación
    await new Promise(resolve => setTimeout(resolve, 1000))

    if (formData.email === VALID_CREDENTIALS.email && formData.password === VALID_CREDENTIALS.password) {
      // Guardar estado de autenticación en localStorage
      localStorage.setItem('isAuthenticated', 'true')
      localStorage.setItem('userEmail', formData.email)
      
      // Redirigir al dashboard
      router.push('/dashboard')
    } else {
      setError('Invalid email or password. Please try again.')
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    if (error) setError('')
  }

  return (
    <>
      <Head>
        <title>Login - Zurich Insurance</title>
        <meta name="description" content="Analyst login" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-blue-800 flex items-center justify-center">
        <div className="max-w-md mx-auto px-4">
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-2">
              Zurich Insurance
            </h1>
            <p className="text-xl text-blue-100">Claims Management System</p>
          </div>
          
          <div className="p-8 bg-white rounded-2xl shadow-2xl border border-slate-100">
            <h2 className="text-3xl font-bold text-slate-800 text-center mb-2">
              Welcome Back
            </h2>
            <p className="text-slate-600 text-center mb-8">
              Sign in to access your dashboard
            </p>
            
            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-600 text-sm">{error}</p>
              </div>
            )}

            {/* Demo Credentials */}
            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-blue-800 text-sm font-medium mb-2">Demo Credentials:</p>
              <p className="text-blue-700 text-xs">Email: analyst@zurich.com</p>
              <p className="text-blue-700 text-xs">Password: zurich2024</p>
            </div>
            
            <form onSubmit={handleSubmit}>
              <div className="mb-6">
                <label className="text-sm font-semibold text-slate-700 mb-2 block">
                  Email Address
                </label>
                <input 
                  type="email" 
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="Enter your email address" 
                  className="w-full p-4 border-2 border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm" 
                  required
                  disabled={loading}
                />
              </div>
              
              <div className="mb-6">
                <label className="text-sm font-semibold text-slate-700 mb-2 block">
                  Password
                </label>
                <input 
                  type="password" 
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Enter your password" 
                  className="w-full p-4 border-2 border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm" 
                  required
                  disabled={loading}
                />
              </div>
              
              <button 
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-4 px-8 rounded-xl font-bold text-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-300 transform hover:scale-105 shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Signing In...' : 'Sign In'}
              </button>
            </form>
          </div>
          
          <div className="text-center mt-8">
            <Link 
              href="/"
              className="text-blue-600 hover:text-blue-700 font-medium transition-colors"
            >
              ← Back to Home
            </Link>
          </div>
        </div>
      </main>
    </>
  )
} 