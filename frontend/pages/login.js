import Head from 'next/head'
import Link from 'next/link'
import { useState } from 'react'

export default function Login() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    // Aquí se conectará con el backend FastAPI para autenticación
    console.log('Login attempt:', formData)
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
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
                />
              </div>
              
              <button 
                type="submit"
                className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-4 px-8 rounded-xl font-bold text-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-300 transform hover:scale-105 shadow-xl"
              >
                Sign In
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