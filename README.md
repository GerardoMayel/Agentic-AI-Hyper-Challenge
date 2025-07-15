# 🤖 Zurich Claims Management System - AI-Powered Insurance Solution

## 🎯 Overview

A comprehensive insurance claims management system built with FastAPI backend and Next.js frontend, featuring AI-powered analysis using Google Gemini, automated email processing, document OCR, and a professional analyst dashboard for final decision making.

## 🚀 Key Features

### 🤖 **AI-Powered Analysis**
- **Sentiment Analysis**: Comprehensive claim sentiment evaluation with risk scoring
- **Traffic Light System**: Visual risk assessment (Red/Yellow/Green)
- **Smart Recommendations**: AI-powered suggestions for investigation steps
- **Document Intelligence**: Advanced OCR with Gemini Vision API
- **Fraud Detection**: Risk factor identification and analysis

### 📧 **Automated Email Processing**
- **Gmail Integration**: Real-time email monitoring and processing
- **Claim Detection**: Automatic identification of claim-related emails
- **Smart Categorization**: Email classification by claim type
- **Auto-Response**: Professional acknowledgment emails
- **Document Extraction**: Automatic attachment processing

### 👤 **Professional Analyst Dashboard**
- **Consolidated View**: One record per claim with complete information
- **Real-time Statistics**: Live dashboard with claim metrics
- **Interactive Analysis**: AI analysis on-demand for each claim
- **Decision Interface**: Professional decision-making tools
- **Status Management**: Complete claim lifecycle tracking

### 📄 **Advanced Document Management**
- **Multi-format Support**: PDF, images, documents
- **OCR Processing**: Text extraction with Gemini Vision
- **Structured Data**: Intelligent data extraction and categorization
- **Cost Analysis**: Automatic cost identification from documents
- **Secure Storage**: Google Cloud Storage integration

## 🏗️ Technical Architecture

### Backend (FastAPI + Python)
```
backend/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Database and configuration
│   ├── models/        # Database models
│   ├── services/      # Business logic services
│   └── static/        # Static files (dashboard)
├── main.py            # FastAPI application
└── requirements.txt   # Python dependencies
```

**Key Services:**
- **LLMService**: Google Gemini AI integration
- **SentimentAnalysisService**: Claim sentiment and risk analysis
- **EnhancedOCRService**: Document processing with Gemini Vision
- **EmailProcessor**: Gmail integration and email processing
- **StorageService**: Google Cloud Storage management

### Frontend (Next.js + React)
```
frontend/
├── pages/             # Next.js pages
├── styles/            # CSS and styling
├── components/        # React components
└── package.json       # Node.js dependencies
```

**Key Pages:**
- **Dashboard**: Main analyst interface
- **Claim Form**: Customer claim submission
- **Analyst Dashboard**: Professional claim management
- **Login**: Secure authentication

### Database (PostgreSQL + SQLite Fallback)
- **Primary**: PostgreSQL on Render
- **Fallback**: SQLite for local development
- **Auto-sync**: Automatic data synchronization
- **Schema Migration**: Alembic for database versioning

## 🗄️ Database Schema

### Core Tables

#### 📧 **emails**
```sql
- id: Primary key
- subject: Email subject
- sender: Sender email
- body: Email content
- received_at: Timestamp
- is_processed: Processing status
- claim_type: Detected claim type
```

#### 🏷️ **claim_submissions**
```sql
- id: Primary key
- claim_number: Auto-generated (CLM-XXXXXXXX)
- customer_name: Customer information
- customer_email: Contact email
- policy_number: Insurance policy
- claim_type: Type of claim
- incident_description: Claim details
- estimated_amount: Claim amount
- status: Current status
- priority: Priority level
- llm_summary: AI analysis summary
- llm_recommendation: AI recommendations
- email_id: Related email reference
```

#### 📄 **document_agent_ocr**
```sql
- id: Primary key
- claim_submission_id: Claim reference
- original_filename: File name
- file_type: Document type
- file_size: File size
- document_type: Classified type
- storage_url: Cloud storage URL
- is_processed: Processing status
- ocr_text: Extracted text
- structured_data: JSON structured data
- inferred_costs: Extracted costs
```

#### 📊 **dashboard_stats**
```sql
- id: Primary key
- total_claims: Total count
- pending_claims: Pending count
- approved_claims: Approved count
- rejected_claims: Rejected count
- closed_claims: Closed count
- total_amount_requested: Financial summary
- total_amount_approved: Approved amounts
- last_updated: Timestamp
```

## 🔧 API Endpoints

### Core Endpoints
```
GET    /health                    # Health check
GET    /api/analyst/claims        # List all claims
GET    /api/analyst/dashboard/stats # Dashboard statistics
POST   /api/analyst/claims/{id}/analyze # AI analysis
PUT    /api/analyst/claims/{id}/status # Update status
GET    /api/analyst/emails        # List processed emails
POST   /api/analyst/claims/{id}/documents # Upload documents
GET    /api/analyst/claims/{id}/documents # List documents
```

### Frontend Routes
```
/                    # Landing page
/login               # Authentication
/dashboard           # Customer dashboard
/claim-form          # Claim submission form
/analyst             # Analyst dashboard (backend)
```

## 🎯 AI Analysis Features

### Sentiment Analysis
- **Risk Scoring**: 0.0-1.0 risk assessment
- **Traffic Light**: Visual risk indicators
- **Priority Levels**: Low/Medium/High/Urgent
- **Confidence Scoring**: AI confidence levels

### Document Intelligence
- **Multi-format OCR**: PDF, images, documents
- **Structured Extraction**: Names, dates, amounts, addresses
- **Cost Analysis**: Automatic cost identification
- **Document Classification**: Smart categorization

### Recommendation Engine
- **Investigation Steps**: Suggested actions
- **Documentation Needs**: Required documents
- **Communication Strategy**: Recommended approach
- **Escalation Logic**: When to escalate

## 🚀 Deployment

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://...

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS_JSON=...
GOOGLE_CLOUD_STORAGE_BUCKET=claims-documents-zurich-ai

# AI Services
GEMINI_API_KEY=...

# Email Services
GMAIL_CREDENTIALS_JSON=...
GMAIL_TOKEN_JSON=...

# Security
SECRET_KEY=...
```

### Production URLs
- **Backend API**: https://zurich-claims-api.onrender.com
- **Frontend**: https://zurich-claims-frontend.onrender.com
- **Analyst Dashboard**: https://zurich-claims-api.onrender.com/analyst

### Local Development
```bash
# Backend
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Frontend
cd frontend
npm run dev
```

## 📊 Supported Claim Types

### Insurance Coverage Types
- **AUTO_INSURANCE**: Vehicle-related claims
- **HOME_INSURANCE**: Property damage claims
- **TRAVEL_INSURANCE**: Travel-related incidents
- **HEALTH_INSURANCE**: Medical claims
- **LIFE_INSURANCE**: Life insurance claims
- **MEDICAL_INSURANCE**: Medical expenses
- **HOTEL_INSURANCE**: Hotel-related incidents
- **OTHER**: Miscellaneous claims

### Document Types
- **POLICE_REPORT**: Law enforcement reports
- **MEDICAL_REPORT**: Medical documentation
- **RECEIPT**: Financial receipts
- **INVOICE**: Billing documents
- **INSURANCE_POLICY**: Policy documents
- **DRIVERS_LICENSE**: Identification
- **PASSPORT**: Travel documents
- **MEDICAL_CERTIFICATE**: Medical certificates
- **TRAVEL_ITINERARY**: Travel plans
- **HOTEL_RECEIPT**: Accommodation receipts
- **FLIGHT_TICKET**: Air travel documents
- **CAR_RENTAL_AGREEMENT**: Vehicle rental
- **OTHER**: Miscellaneous documents

## 🔐 Security Features

### Data Protection
- **Encrypted Storage**: Google Cloud Storage encryption
- **Secure Database**: PostgreSQL with access controls
- **API Security**: FastAPI with input validation
- **Authentication**: Secure login system

### Compliance
- **Audit Trail**: Complete decision tracking
- **Analyst Accountability**: All decisions recorded
- **Data Privacy**: Customer information protection
- **Professional Standards**: Insurance industry compliance

## 📈 Benefits

### For Insurance Companies
- **70-80% Time Reduction**: Automated processing
- **AI-Powered Insights**: Better decision quality
- **Compliance Assurance**: Automated documentation
- **Scalability**: High-volume claim handling

### For Analysts
- **Comprehensive Tools**: All information in one interface
- **AI Support**: Intelligent recommendations
- **Efficiency**: Streamlined workflow
- **Professional Interface**: Modern, responsive design

### For Customers
- **Faster Processing**: Quick claim resolution
- **Better Communication**: Professional responses
- **Transparency**: Clear decision reasoning
- **Consistency**: Fair claim handling

## 🔮 Future Enhancements

### Planned Features
- **Machine Learning**: Historical data training
- **Predictive Analytics**: Outcome prediction
- **Advanced Reporting**: Detailed analytics
- **Mobile App**: Native mobile application

### Integration Opportunities
- **External Systems**: Third-party integrations
- **Fraud Detection**: Advanced algorithms
- **Customer Portal**: Self-service features
- **API Expansion**: Public API access

## 📞 Support & Documentation

### API Documentation
- **Interactive Docs**: Available at `/docs`
- **Health Check**: System status at `/health`
- **OpenAPI Spec**: Complete API specification

### Technical Support
- **GitHub Repository**: Complete source code
- **Deployment Guide**: Step-by-step instructions
- **Configuration**: Environment setup guide

---

**Status:** ✅ Production Ready  
**Last Updated:** July 2025  
**Version:** 2.0.0  
**Technology Stack:** FastAPI, Next.js, PostgreSQL, Google Gemini AI, Google Cloud Storage
