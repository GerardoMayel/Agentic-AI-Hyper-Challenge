-- Script SQL para crear las tablas del sistema de procesamiento de emails y claims
-- Ejecutar en pgAdmin o psql

-- 1. Tabla EMAILS para almacenar emails recibidos
CREATE TABLE IF NOT EXISTS EMAILS (
    id SERIAL PRIMARY KEY,
    gmail_id VARCHAR(255) UNIQUE NOT NULL,
    thread_id VARCHAR(255) NOT NULL,
    from_email VARCHAR(255) NOT NULL,
    to_email VARCHAR(255) NOT NULL,
    subject VARCHAR(500) NOT NULL,
    body_text TEXT,
    body_html TEXT,
    received_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE,
    is_processed BOOLEAN DEFAULT FALSE,
    is_first_notification BOOLEAN
);

-- 2. Tabla CLAIM_SUBMISSIONS para siniestros creados desde emails
CREATE TABLE IF NOT EXISTS CLAIM_SUBMISSIONS (
    id SERIAL PRIMARY KEY,
    claim_number VARCHAR(50) UNIQUE NOT NULL,
    email_id INTEGER NOT NULL REFERENCES EMAILS(id),
    customer_name VARCHAR(200) NOT NULL,
    customer_email VARCHAR(200) NOT NULL,
    policy_number VARCHAR(100),
    claim_type VARCHAR(100) NOT NULL,
    incident_date TIMESTAMP,
    incident_description TEXT,
    estimated_amount DECIMAL(10,2),
    status VARCHAR(50) DEFAULT 'PENDING',
    priority VARCHAR(20) DEFAULT 'NORMAL',
    llm_summary TEXT,
    llm_recommendation VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP WITH TIME ZONE
);

-- 3. Tabla DOCUMENTS_AGENT_OCR para documentos procesados con OCR
CREATE TABLE IF NOT EXISTS DOCUMENTS_AGENT_OCR (
    id SERIAL PRIMARY KEY,
    claim_submission_id INTEGER NOT NULL REFERENCES CLAIM_SUBMISSIONS(id),
    email_id INTEGER REFERENCES EMAILS(id),
    original_filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(100) NOT NULL,
    file_size INTEGER NOT NULL,
    storage_url VARCHAR(500) NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    ocr_text TEXT,
    structured_data JSONB,
    image_description JSONB,
    document_type VARCHAR(100),
    inferred_costs JSONB,
    is_processed BOOLEAN DEFAULT FALSE,
    processing_errors TEXT,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE
);

-- 4. Tabla CLAIM_STATUS_UPDATES para seguimiento de cambios de estado
CREATE TABLE IF NOT EXISTS CLAIM_STATUS_UPDATES (
    id SERIAL PRIMARY KEY,
    claim_submission_id INTEGER NOT NULL REFERENCES CLAIM_SUBMISSIONS(id),
    old_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    reason TEXT,
    analyst_name VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabla DASHBOARD_STATS para estadísticas del dashboard
CREATE TABLE IF NOT EXISTS DASHBOARD_STATS (
    id SERIAL PRIMARY KEY,
    total_claims INTEGER DEFAULT 0,
    pending_claims INTEGER DEFAULT 0,
    approved_claims INTEGER DEFAULT 0,
    rejected_claims INTEGER DEFAULT 0,
    closed_claims INTEGER DEFAULT 0,
    total_amount_requested DECIMAL(15,2) DEFAULT 0.0,
    total_amount_approved DECIMAL(15,2) DEFAULT 0.0,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_emails_gmail_id ON EMAILS(gmail_id);
CREATE INDEX IF NOT EXISTS idx_emails_thread_id ON EMAILS(thread_id);
CREATE INDEX IF NOT EXISTS idx_emails_processed ON EMAILS(is_processed);
CREATE INDEX IF NOT EXISTS idx_emails_received_at ON EMAILS(received_at);

CREATE INDEX IF NOT EXISTS idx_claims_claim_number ON CLAIM_SUBMISSIONS(claim_number);
CREATE INDEX IF NOT EXISTS idx_claims_email_id ON CLAIM_SUBMISSIONS(email_id);
CREATE INDEX IF NOT EXISTS idx_claims_status ON CLAIM_SUBMISSIONS(status);
CREATE INDEX IF NOT EXISTS idx_claims_priority ON CLAIM_SUBMISSIONS(priority);
CREATE INDEX IF NOT EXISTS idx_claims_created_at ON CLAIM_SUBMISSIONS(created_at);

CREATE INDEX IF NOT EXISTS idx_documents_claim_id ON DOCUMENTS_AGENT_OCR(claim_submission_id);
CREATE INDEX IF NOT EXISTS idx_documents_email_id ON DOCUMENTS_AGENT_OCR(email_id);
CREATE INDEX IF NOT EXISTS idx_documents_type ON DOCUMENTS_AGENT_OCR(document_type);
CREATE INDEX IF NOT EXISTS idx_documents_processed ON DOCUMENTS_AGENT_OCR(is_processed);

CREATE INDEX IF NOT EXISTS idx_status_updates_claim_id ON CLAIM_STATUS_UPDATES(claim_submission_id);
CREATE INDEX IF NOT EXISTS idx_status_updates_created_at ON CLAIM_STATUS_UPDATES(created_at);

-- Insertar registro inicial en DASHBOARD_STATS
INSERT INTO DASHBOARD_STATS (total_claims, pending_claims, approved_claims, rejected_claims, closed_claims, total_amount_requested, total_amount_approved)
VALUES (0, 0, 0, 0, 0, 0.0, 0.0)
ON CONFLICT DO NOTHING;

-- Comentarios sobre las tablas
COMMENT ON TABLE EMAILS IS 'Almacena emails recibidos con información de Gmail y estado de procesamiento';
COMMENT ON TABLE CLAIM_SUBMISSIONS IS 'Siniestros creados automáticamente desde emails procesados';
COMMENT ON TABLE DOCUMENTS_AGENT_OCR IS 'Documentos adjuntos procesados con OCR y análisis de IA';
COMMENT ON TABLE CLAIM_STATUS_UPDATES IS 'Historial de cambios de estado de los siniestros';
COMMENT ON TABLE DASHBOARD_STATS IS 'Estadísticas agregadas para el dashboard de analistas'; 