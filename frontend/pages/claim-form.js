import Head from 'next/head'
import Link from 'next/link'
import { useState, useCallback } from 'react'

// Component: Claim Type
function ClaimType({ claimType, onChange }) {
  return (
    <div className="p-6 sm:p-8 bg-white rounded-xl shadow-lg border border-gray-100">
      <h3 className="text-xl sm:text-2xl font-bold text-slate-800 mb-6">Claim Type</h3>
      <div className="space-y-4">
        {['Trip Cancellation', 'Trip Delay', 'Trip Interruption'].map((type) => (
          <label key={type} className="flex items-center space-x-3 cursor-pointer">
            <input
              type="radio"
              name="claimType"
              value={type}
              checked={claimType === type}
              onChange={(e) => onChange('claimType', e.target.value)}
              className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
              required
            />
            <span className="text-slate-700 font-medium">{type}</span>
          </label>
        ))}
      </div>
    </div>
  )
}

// Component: Claimant Information
function ClaimantInfo({ data, onChange }) {
  return (
    <div className="p-6 sm:p-8 bg-white rounded-xl shadow-lg border border-gray-100">
      <h3 className="text-xl sm:text-2xl font-bold text-slate-800 mb-6">Claimant Information</h3>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        <div>
          <label className="text-sm font-semibold text-slate-700 mb-2 block">
            Full Name *
          </label>
          <input
            type="text"
            value={data.fullName}
            onChange={(e) => onChange('fullName', e.target.value)}
            placeholder="Full name"
            className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
            required
          />
        </div>
        
        <div>
          <label className="text-sm font-semibold text-slate-700 mb-2 block">
            Email Address *
          </label>
          <input
            type="email"
            value={data.email}
            onChange={(e) => onChange('email', e.target.value)}
            placeholder="your.email@example.com"
            className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
            required
          />
        </div>

        <div className="lg:col-span-2">
          <label className="text-sm font-semibold text-slate-700 mb-2 block">
            Address *
          </label>
          <textarea
            value={data.address}
            onChange={(e) => onChange('address', e.target.value)}
            placeholder="Complete address"
            rows={3}
            className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
            required
          />
        </div>

        <div>
          <label className="text-sm font-semibold text-slate-700 mb-2 block">
            City *
          </label>
          <input
            type="text"
            value={data.city}
            onChange={(e) => onChange('city', e.target.value)}
            placeholder="City"
            className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
            required
          />
        </div>

        <div>
          <label className="text-sm font-semibold text-slate-700 mb-2 block">
            State/Province *
          </label>
          <input
            type="text"
            value={data.state}
            onChange={(e) => onChange('state', e.target.value)}
            placeholder="State or province"
            className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
            required
          />
        </div>

        <div>
          <label className="text-sm font-semibold text-slate-700 mb-2 block">
            Zip Code *
          </label>
          <input
            type="text"
            value={data.zipCode}
            onChange={(e) => onChange('zipCode', e.target.value)}
            placeholder="Zip code"
            className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
            required
          />
        </div>

        <div>
          <label className="text-sm font-semibold text-slate-700 mb-2 block">
            Mobile Phone *
          </label>
          <input
            type="tel"
            value={data.mobilePhone}
            onChange={(e) => onChange('mobilePhone', e.target.value)}
            placeholder="+1 (555) 123-4567"
            className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
            required
          />
        </div>

        <div>
          <label className="text-sm font-semibold text-slate-700 mb-2 block">
            Other Phone
          </label>
          <input
            type="tel"
            value={data.otherPhone}
            onChange={(e) => onChange('otherPhone', e.target.value)}
            placeholder="Alternative phone"
            className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
          />
        </div>

        <div className="lg:col-span-2">
          <label className="text-sm font-semibold text-slate-700 mb-2 block">
            Names of All Claimants *
          </label>
          <textarea
            value={data.allClaimants}
            onChange={(e) => onChange('allClaimants', e.target.value)}
            placeholder="List of all names of people making the claim"
            rows={3}
            className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
            required
          />
        </div>

        <div>
          <label className="text-sm font-semibold text-slate-700 mb-2 block">
            Policy Number *
          </label>
          <input
            type="text"
            value={data.policyNumber}
            onChange={(e) => onChange('policyNumber', e.target.value)}
            placeholder="Policy number or confirmation"
            className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
            required
          />
        </div>

        <div>
          <label className="text-sm font-semibold text-slate-700 mb-2 block">
            Insurance Agency *
          </label>
          <input
            type="text"
            value={data.insuranceAgency}
            onChange={(e) => onChange('insuranceAgency', e.target.value)}
            placeholder="Name of agency/company"
            className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
            required
          />
        </div>

        <div>
          <label className="text-sm font-semibold text-slate-700 mb-2 block">
            Initial Deposit Date *
          </label>
          <input
            type="date"
            value={data.initialDepositDate}
            onChange={(e) => onChange('initialDepositDate', e.target.value)}
            className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
            required
          />
        </div>
      </div>
    </div>
  )
}

// Component: Incident Details
function IncidentDetails({ data, onChange, totalAmount }) {
  return (
    <div className="p-6 sm:p-8 bg-white rounded-xl shadow-lg border border-gray-100">
      <h3 className="text-xl sm:text-2xl font-bold text-slate-800 mb-6">Incident Details</h3>
      <div className="space-y-6">
        <div>
          <label className="text-sm font-semibold text-slate-700 mb-2 block">
            Detailed Incident Description *
          </label>
          <textarea
            value={data.incidentDescription}
            onChange={(e) => onChange('incidentDescription', e.target.value)}
            placeholder="Describe in detail what happened, when, where and why..."
            rows={6}
            minLength={50}
            className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
            required
          />
          <p className="text-sm text-gray-500 mt-1">
            Minimum 50 characters. Current: {data.incidentDescription.length}
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
          <div>
            <label className="text-sm font-semibold text-slate-700 mb-2 block">
              Loss Date *
            </label>
            <input
              type="date"
              value={data.lossDate}
              onChange={(e) => onChange('lossDate', e.target.value)}
              className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
              required
            />
          </div>

          <div>
            <label className="text-sm font-semibold text-slate-700 mb-2 block">
              Total Amount Requested (USD)
            </label>
            <input
              type="number"
              value={totalAmount.toFixed(2)}
              disabled
              className="w-full p-3 border-2 border-gray-200 rounded-lg bg-gray-50 text-gray-700 font-semibold"
            />
            <p className="text-sm text-gray-500 mt-1">
              Automatically calculated from expense breakdown
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

// Component: Expense Breakdown
function ExpenseBreakdown({ expenses, onAddExpense, onRemoveExpense, onUpdateExpense }) {
  return (
    <div className="p-6 sm:p-8 bg-white rounded-xl shadow-lg border border-gray-100">
      <h3 className="text-xl sm:text-2xl font-bold text-slate-800 mb-6">Expense Breakdown</h3>
      
      <div className="space-y-4">
        {expenses.map((expense, index) => (
          <div key={index} className="grid grid-cols-1 xl:grid-cols-4 gap-4 p-4 border border-gray-200 rounded-lg">
            <div>
              <label className="text-sm font-semibold text-slate-700 mb-2 block">
                Description *
              </label>
              <input
                type="text"
                value={expense.description}
                onChange={(e) => onUpdateExpense(index, 'description', e.target.value)}
                placeholder="Expense description"
                className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500/20 focus:border-blue-600"
                required
              />
            </div>
            
            <div>
              <label className="text-sm font-semibold text-slate-700 mb-2 block">
                Date *
              </label>
              <input
                type="date"
                value={expense.date}
                onChange={(e) => onUpdateExpense(index, 'date', e.target.value)}
                className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500/20 focus:border-blue-600"
                required
              />
            </div>
            
            <div>
              <label className="text-sm font-semibold text-slate-700 mb-2 block">
                Amount (USD) *
              </label>
              <input
                type="number"
                value={expense.amount}
                onChange={(e) => onUpdateExpense(index, 'amount', parseFloat(e.target.value) || 0)}
                placeholder="0.00"
                step="0.01"
                min="0"
                className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500/20 focus:border-blue-600"
                required
              />
            </div>
            
            <div className="flex items-end">
              <button
                type="button"
                onClick={() => onRemoveExpense(index)}
                className="w-full p-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
              >
                Remove
              </button>
            </div>
          </div>
        ))}
      </div>

      <button
        type="button"
        onClick={onAddExpense}
        className="mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
      >
        + Add Expense
      </button>
    </div>
  )
}

// Component: Documentation Upload
function DocumentationUpload({ files, onFileSelect, onRemoveFile, onTakePhoto }) {
  return (
    <div className="p-6 sm:p-8 bg-white rounded-xl shadow-lg border border-gray-100">
      <h3 className="text-xl sm:text-2xl font-bold text-slate-800 mb-6">Documentation Upload</h3>
      
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <label className="cursor-pointer">
            <input
              type="file"
              multiple
              accept=".pdf,.png,.jpg,.jpeg"
              onChange={onFileSelect}
              className="hidden"
            />
            <div className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium text-center">
              📁 Upload Files
            </div>
          </label>
          
          <button
            type="button"
            onClick={onTakePhoto}
            className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
          >
            📸 Take Photo
          </button>
        </div>

        {files.length > 0 && (
          <div className="mt-6">
            <h4 className="text-lg font-semibold text-slate-700 mb-3">Selected Files:</h4>
            <ul className="space-y-2">
              {files.map((file, index) => (
                <li key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm text-slate-700 truncate">{file.name}</span>
                  <button
                    type="button"
                    onClick={() => onRemoveFile(index)}
                    className="text-red-500 hover:text-red-700 font-bold ml-2"
                  >
                    ✕
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

// Component: Authorization and Signature
function Authorization({ data, onChange }) {
  return (
    <div className="p-6 sm:p-8 bg-white rounded-xl shadow-lg border border-gray-100">
      <h3 className="text-xl sm:text-2xl font-bold text-slate-800 mb-6">Authorization and Signature</h3>
      
      <div className="space-y-6">
        <div className="flex items-start space-x-3">
          <input
            type="checkbox"
            checked={data.authorization}
            onChange={(e) => onChange('authorization', e.target.checked)}
            className="mt-1 w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            required
          />
          <label className="text-sm text-slate-700">
            I declare that the above information is true, complete and correct. *
          </label>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
          <div>
            <label className="text-sm font-semibold text-slate-700 mb-2 block">
              Signature (Full Name) *
            </label>
            <input
              type="text"
              value={data.signature}
              onChange={(e) => onChange('signature', e.target.value)}
              placeholder="Type your full name"
              className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
              required
            />
          </div>

          <div>
            <label className="text-sm font-semibold text-slate-700 mb-2 block">
              Signature Date *
            </label>
            <input
              type="date"
              value={data.signatureDate}
              onChange={(e) => onChange('signatureDate', e.target.value)}
              className="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300"
              required
            />
          </div>
        </div>
      </div>
    </div>
  )
}

// Main Component: Claim Form
export default function ClaimForm() {
  const [formData, setFormData] = useState({
    // Claim type
    claimType: '',
    
    // Claimant information
    fullName: '',
    email: '',
    address: '',
    city: '',
    state: '',
    zipCode: '',
    mobilePhone: '',
    otherPhone: '',
    allClaimants: '',
    policyNumber: '',
    insuranceAgency: '',
    initialDepositDate: '',
    
    // Incident details
    incidentDescription: '',
    lossDate: '',
    
    // Authorization
    authorization: false,
    signature: '',
    signatureDate: new Date().toISOString().split('T')[0]
  })

  const [expenses, setExpenses] = useState([
    { description: '', date: '', amount: 0 }
  ])

  const [files, setFiles] = useState([])

  const handleChange = useCallback((field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }, [])

  const addExpense = useCallback(() => {
    setExpenses(prev => [...prev, { description: '', date: '', amount: 0 }])
  }, [])

  const removeExpense = useCallback((index) => {
    setExpenses(prev => prev.filter((_, i) => i !== index))
  }, [])

  const updateExpense = useCallback((index, field, value) => {
    setExpenses(prev => prev.map((expense, i) => 
      i === index ? { ...expense, [field]: value } : expense
    ))
  }, [])

  const handleFileSelect = useCallback((e) => {
    const selectedFiles = Array.from(e.target.files)
    setFiles(prev => [...prev, ...selectedFiles])
  }, [])

  const removeFile = useCallback((index) => {
    setFiles(prev => prev.filter((_, i) => i !== index))
  }, [])

  const takePhoto = useCallback(() => {
    // Camera functionality simulation (in production would use navigator.mediaDevices.getUserMedia)
    alert('Camera functionality will be implemented in the final version')
  }, [])

  const totalAmount = expenses.reduce((sum, expense) => sum + (expense.amount || 0), 0)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Additional validations
    if (expenses.length === 0) {
      alert('You must add at least one expense')
      return
    }

    if (files.length === 0) {
      alert('You must upload at least one document')
      return
    }

    try {
      // Preparar datos del claim para el backend
      const claimData = {
        coverage_type: formData.claimType,
        full_name: formData.fullName,
        email: formData.email,
        phone: formData.mobilePhone,
        policy_number: formData.policyNumber,
        incident_date: formData.lossDate ? new Date(formData.lossDate).isoformat() : null,
        incident_location: `${formData.address}, ${formData.city}, ${formData.state} ${formData.zipCode}`,
        description: formData.incidentDescription,
        estimated_amount: totalAmount
      }

      // 1. Crear el claim en el backend
      console.log('Sending claim data to backend:', claimData)
      
      const claimResponse = await fetch('http://localhost:8000/api/claims', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(claimData)
      })

      if (!claimResponse.ok) {
        throw new Error(`Error creating claim: ${claimResponse.statusText}`)
      }

      const claimResult = await claimResponse.json()
      console.log('Claim created:', claimResult)

      if (!claimResult.success) {
        throw new Error(claimResult.message || 'Failed to create claim')
      }

      const claimId = claimResult.data.claim_id
      console.log('Claim ID generated:', claimId)

      // 2. Subir documentos
      console.log('Uploading documents...')
      
      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        const formData = new FormData()
        formData.append('file', file)
        formData.append('document_type', `DOCUMENT_${i + 1}`)
        formData.append('upload_notes', `Uploaded via web form - ${file.name}`)

        const documentResponse = await fetch(`http://localhost:8000/api/claims/${claimId}/documents`, {
          method: 'POST',
          body: formData
        })

        if (!documentResponse.ok) {
          console.warn(`Warning: Failed to upload document ${file.name}: ${documentResponse.statusText}`)
        } else {
          const documentResult = await documentResponse.json()
          console.log(`Document ${file.name} uploaded:`, documentResult)
        }
      }

      // 3. Mostrar éxito
      alert(`Claim submitted successfully!\n\nClaim ID: ${claimId}\n\nYour claim has been created and documents uploaded. You will receive a confirmation email shortly.`)
      
      // 4. Limpiar formulario (opcional)
      // window.location.href = '/dashboard' // Redirigir al dashboard
      
    } catch (error) {
      console.error('Error submitting claim:', error)
      alert(`Error submitting claim: ${error.message}`)
    }
  }

  return (
    <>
      <Head>
        <title>Submit Claim - Zurich Insurance</title>
        <meta name="description" content="Submit your insurance claim" />
      </Head>

      <main className="min-h-screen">
        {/* Header */}
        <div className="w-full py-12 sm:py-20 bg-gradient-to-br from-slate-800 via-blue-900 to-slate-900 shadow-2xl">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 text-center">
            <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-4">
              Claims Management System
            </h1>
            <p className="text-lg sm:text-xl text-blue-100 mb-2">Insurance Claim Submission</p>
            <p className="text-base sm:text-lg text-gray-300">
              Complete all sections below to submit your claim for processing
            </p>
          </div>
        </div>

        {/* Form */}
        <div className="w-full py-8 sm:py-16 bg-gray-50">
          <div className="max-w-6xl mx-auto px-4">
            <form onSubmit={handleSubmit} className="space-y-6 sm:space-y-8">
              <ClaimType 
                claimType={formData.claimType} 
                onChange={handleChange} 
              />
              
              <ClaimantInfo 
                data={formData} 
                onChange={handleChange} 
              />
              
              <ExpenseBreakdown 
                expenses={expenses}
                onAddExpense={addExpense}
                onRemoveExpense={removeExpense}
                onUpdateExpense={updateExpense}
              />
              
              <IncidentDetails 
                data={formData} 
                onChange={handleChange}
                totalAmount={totalAmount}
              />
              
              <DocumentationUpload 
                files={files}
                onFileSelect={handleFileSelect}
                onRemoveFile={removeFile}
                onTakePhoto={takePhoto}
              />
              
              <Authorization 
                data={formData} 
                onChange={handleChange} 
              />

              {/* Submit Button */}
              <div className="text-center pt-6 sm:pt-8">
                <button 
                  type="submit"
                  className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-8 sm:px-12 py-3 sm:py-4 rounded-xl font-bold text-lg sm:text-xl hover:from-blue-700 hover:to-blue-800 transition-all duration-300 transform hover:scale-105 shadow-xl"
                >
                  Submit Claim
                </button>
              </div>
            </form>

            {/* Back Link */}
            <div className="text-center mt-6 sm:mt-8">
              <Link 
                href="/"
                className="text-blue-600 hover:text-blue-700 font-medium transition-colors"
              >
                ← Back to Home
              </Link>
            </div>
          </div>
        </div>
      </main>
    </>
  )
} 