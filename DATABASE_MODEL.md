# 🗄️ COMPLETE DATABASE MODEL - AI-Powered Claims Management System

## 📋 **SYSTEM OVERVIEW**

Complete automated insurance claims processing system that:
1. **Monitors** incoming emails for claim-related content
2. **Extracts** comprehensive information using AI analysis
3. **Processes** documents with OCR and intelligent analysis
4. **Provides** AI recommendations for human analyst review
5. **Records** human analyst final decisions and rulings
6. **Maintains** complete audit trail of all processing steps

---

## 🗂️ **COMPLETE TABLE STRUCTURE**

### 📧 **Table 1: EMAILS**
```sql
CREATE TABLE EMAILS (
    id SERIAL PRIMARY KEY,
    gmail_id VARCHAR(255) UNIQUE NOT NULL,
    thread_id VARCHAR(255),
    from_email VARCHAR(255) NOT NULL,
    to_email VARCHAR(255) NOT NULL,
    subject TEXT NOT NULL,
    body_text TEXT,
    body_html TEXT,
    snippet TEXT,
    received_at TIMESTAMP WITH TIME ZONE NOT NULL,
    processed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE,
    is_first_notification BOOLEAN DEFAULT FALSE,
    metadata JSONB,
    headers JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** Stores all incoming emails with claim-related content for processing and analysis.

### 🏷️ **Table 2: CLAIM_SUBMISSIONS**
```sql
CREATE TABLE CLAIM_SUBMISSIONS (
    id SERIAL PRIMARY KEY,
    claim_number VARCHAR(50) UNIQUE NOT NULL DEFAULT generate_claim_number(),
    email_id INTEGER NOT NULL REFERENCES EMAILS(id),
    
    -- Customer Information
    customer_name VARCHAR(200) NOT NULL,
    customer_email VARCHAR(200) NOT NULL,
    policy_number VARCHAR(100),
    
    -- Claim Details
    claim_type VARCHAR(100) NOT NULL,
    incident_date TIMESTAMP WITH TIME ZONE,
    incident_description TEXT,
    estimated_amount DECIMAL(15,2),
    
    -- Status and Processing
    status VARCHAR(50) DEFAULT 'PENDING',
    priority VARCHAR(20) DEFAULT 'NORMAL',
    
    -- AI Analysis Results
    llm_summary TEXT,
    llm_recommendation VARCHAR(100),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP WITH TIME ZONE
);
```

**Purpose:** Main claims table with comprehensive information extracted by AI and human decisions.

### 📄 **Table 3: DOCUMENTS_AGENT_OCR**
```sql
CREATE TABLE DOCUMENTS_AGENT_OCR (
    id SERIAL PRIMARY KEY,
    claim_submission_id INTEGER NOT NULL REFERENCES CLAIM_SUBMISSIONS(id),
    email_id INTEGER REFERENCES EMAILS(id),
    
    -- File Information
    original_filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(100) NOT NULL,
    file_size INTEGER NOT NULL,
    storage_url VARCHAR(500) NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    
    -- OCR and AI Processing
    ocr_text TEXT,
    structured_data JSONB,
    image_description JSONB,
    document_type VARCHAR(100),
    inferred_costs JSONB,
    
    -- Processing Status
    is_processed BOOLEAN DEFAULT FALSE,
    processing_errors TEXT,
    
    -- Timestamps
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE
);
```

**Purpose:** Document management with OCR processing and AI analysis for intelligent document understanding.

### 📈 **Table 4: CLAIM_STATUS_UPDATES**
```sql
CREATE TABLE CLAIM_STATUS_UPDATES (
    id SERIAL PRIMARY KEY,
    claim_submission_id INTEGER NOT NULL REFERENCES CLAIM_SUBMISSIONS(id),
    
    -- Status Change Information
    old_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    reason TEXT,
    
    -- Human Analyst Accountability
    analyst_name VARCHAR(200),
    
    -- Timestamp
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** Complete audit trail of all status changes with human analyst accountability for final decisions.

### 📊 **Table 5: DASHBOARD_STATS**
```sql
CREATE TABLE DASHBOARD_STATS (
    id SERIAL PRIMARY KEY,
    
    -- Claim Statistics
    total_claims INTEGER DEFAULT 0,
    pending_claims INTEGER DEFAULT 0,
    approved_claims INTEGER DEFAULT 0,
    rejected_claims INTEGER DEFAULT 0,
    closed_claims INTEGER DEFAULT 0,
    
    -- Financial Statistics
    total_amount_requested DECIMAL(15,2) DEFAULT 0.0,
    total_amount_approved DECIMAL(15,2) DEFAULT 0.0,
    
    -- Timestamp
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** Real-time statistics for the analyst dashboard with financial and processing metrics.

---

## 🔗 **RELATIONSHIPS**

### Primary Relationships
- **EMAILS** → **CLAIM_SUBMISSIONS** (One-to-One)
  - Each email can create one claim submission
  - Email ID is required for claim creation

- **CLAIM_SUBMISSIONS** → **DOCUMENTS_AGENT_OCR** (One-to-Many)
  - Each claim can have multiple documents
  - Documents are linked to specific claims

- **CLAIM_SUBMISSIONS** → **CLAIM_STATUS_UPDATES** (One-to-Many)
  - Each claim can have multiple status updates
  - Complete history of all status changes

### Data Flow
1. **Email Received** → Stored in EMAILS table
2. **AI Processing** → Creates CLAIM_SUBMISSIONS record
3. **Document Upload** → Creates DOCUMENTS_AGENT_OCR records
4. **Status Changes** → Creates CLAIM_STATUS_UPDATES records
5. **Statistics Update** → Updates DASHBOARD_STATS

---

## 🎯 **HUMAN DECISION PROCESS**

### AI Analysis Phase
- **LLM Analysis**: Comprehensive claim evaluation using Gemini AI
- **Document Processing**: OCR and intelligent document analysis
- **Risk Assessment**: Fraud detection and risk evaluation
- **Recommendations**: AI suggestions for human review

### Human Decision Phase
- **Analyst Review**: Human analyst reviews AI analysis
- **Final Decision**: Human makes final ruling and decision
- **Professional Reasoning**: Required justification for decision
- **Accountability**: Analyst name recorded with all decisions

### Decision Workflow
1. **Email Processing** → Automatic email analysis
2. **AI Analysis** → LLM provides comprehensive recommendations
3. **Human Review** → Analyst reviews AI analysis and claim details
4. **Final Decision** → Human analyst makes final ruling
5. **Documentation** → Complete audit trail with reasoning

---

## 📊 **KEY FEATURES**

### Automated Processing
- **Email Monitoring**: Automatic detection of claim-related emails
- **AI Extraction**: Intelligent information extraction from emails
- **Document Analysis**: OCR and AI-powered document processing
- **Status Tracking**: Complete workflow status management

### Human Interface
- **Analyst Dashboard**: Complete web interface for claim management
- **Consolidated View**: One record per claim with all information
- **Decision Interface**: Clear interface for human rulings
- **Audit Trail**: Complete tracking of all decisions and changes

### AI Integration
- **Comprehensive Analysis**: Multi-dimensional claim evaluation
- **Risk Assessment**: Fraud detection and risk evaluation
- **Document Intelligence**: OCR and structured data extraction
- **Recommendation Engine**: AI-powered suggestions for human review

---

## 🔐 **SECURITY & COMPLIANCE**

### Data Protection
- **Secure Storage**: Google Cloud Storage with encryption
- **Database Security**: PostgreSQL with proper access controls
- **API Security**: FastAPI with input validation and sanitization

### Compliance Features
- **Audit Trail**: Complete tracking of all decisions and changes
- **Analyst Accountability**: All decisions recorded with analyst name
- **Data Privacy**: Proper handling of customer information
- **Status History**: Complete history of all status changes

---

## 📈 **PERFORMANCE OPTIMIZATION**

### Indexes
```sql
-- Email processing indexes
CREATE INDEX idx_emails_gmail_id ON EMAILS(gmail_id);
CREATE INDEX idx_emails_thread_id ON EMAILS(thread_id);
CREATE INDEX idx_emails_processed ON EMAILS(is_processed);
CREATE INDEX idx_emails_received_at ON EMAILS(received_at);

-- Claim processing indexes
CREATE INDEX idx_claims_number ON CLAIM_SUBMISSIONS(claim_number);
CREATE INDEX idx_claims_status ON CLAIM_SUBMISSIONS(status);
CREATE INDEX idx_claims_priority ON CLAIM_SUBMISSIONS(priority);
CREATE INDEX idx_claims_created_at ON CLAIM_SUBMISSIONS(created_at);

-- Document processing indexes
CREATE INDEX idx_documents_claim_id ON DOCUMENTS_AGENT_OCR(claim_submission_id);
CREATE INDEX idx_documents_type ON DOCUMENTS_AGENT_OCR(document_type);
CREATE INDEX idx_documents_processed ON DOCUMENTS_AGENT_OCR(is_processed);

-- Status tracking indexes
CREATE INDEX idx_status_updates_claim_id ON CLAIM_STATUS_UPDATES(claim_submission_id);
CREATE INDEX idx_status_updates_created_at ON CLAIM_STATUS_UPDATES(created_at);
```

### Query Optimization
- **Efficient Joins**: Optimized relationships for fast data retrieval
- **Pagination**: Large dataset handling with proper pagination
- **Caching**: Strategic caching for frequently accessed data
- **Background Processing**: Asynchronous processing for heavy operations

---

## 🚀 **DEPLOYMENT CONSIDERATIONS**

### Database Configuration
- **PostgreSQL 16.9**: Latest stable version with advanced features
- **Connection Pooling**: Efficient connection management
- **Backup Strategy**: Automated backups with point-in-time recovery
- **Monitoring**: Database performance monitoring and alerting

### Scalability
- **Horizontal Scaling**: Read replicas for query distribution
- **Vertical Scaling**: Resource optimization for growing workloads
- **Partitioning**: Large table partitioning for performance
- **Archiving**: Historical data archiving strategies

---

**Status:** ✅ Production Ready  
**Last Updated:** December 2024  
**Version:** 1.0.0 