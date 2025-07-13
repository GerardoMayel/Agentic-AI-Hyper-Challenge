-- Script SQL para insertar datos de prueba y validar el funcionamiento
-- Ejecutar en pgAdmin o psql después de crear y validar las tablas

-- 1. Insertar emails de prueba
INSERT INTO EMAILS (gmail_id, thread_id, from_email, to_email, subject, body_text, is_first_notification) VALUES
('gmail_001', 'thread_001', 'cliente1@example.com', 'claims@zurich.com', 'Siniestro de viaje - Vuelo cancelado', 'Hola, tuve un problema con mi vuelo y necesito presentar un siniestro. Adjunto los documentos.', TRUE),
('gmail_002', 'thread_002', 'cliente2@example.com', 'claims@zurich.com', 'Reclamo por hotel - Problemas de habitación', 'Buenos días, tuve problemas con mi habitación de hotel y quiero presentar un reclamo.', TRUE),
('gmail_003', 'thread_001', 'cliente1@example.com', 'claims@zurich.com', 'Re: Siniestro de viaje - Documentos adicionales', 'Aquí están los documentos adicionales que solicitaste.', FALSE);

-- 2. Insertar claim submissions de prueba
INSERT INTO CLAIM_SUBMISSIONS (claim_number, email_id, customer_name, customer_email, policy_number, claim_type, incident_date, incident_description, estimated_amount, status, priority, llm_summary, llm_recommendation) VALUES
('CLM-A1B2C3D4', 1, 'Juan Pérez', 'cliente1@example.com', 'POL-2024-001', 'TRAVEL_INSURANCE', '2024-01-15 10:30:00', 'Vuelo cancelado por mal tiempo, pérdida de conexión', 1500.00, 'PENDING', 'NORMAL', 'Cliente reporta cancelación de vuelo por mal tiempo. Documentos adjuntos incluyen boletos y comprobantes de gastos adicionales.', 'REQUEST_MORE_DOCS'),
('CLM-E5F6G7H8', 2, 'María García', 'cliente2@example.com', 'POL-2024-002', 'HOTEL_INSURANCE', '2024-01-20 14:00:00', 'Habitación con problemas de limpieza y ruido excesivo', 800.00, 'UNDER_REVIEW', 'HIGH', 'Cliente reporta problemas con habitación de hotel. Solicita compensación por mala experiencia.', 'APPROVE');

-- 3. Insertar documentos de prueba
INSERT INTO DOCUMENTS_AGENT_OCR (claim_submission_id, email_id, original_filename, file_type, file_size, storage_url, storage_path, ocr_text, document_type, is_processed) VALUES
(1, 1, 'boleto_vuelo.pdf', 'application/pdf', 245760, 'https://storage.googleapis.com/bucket/boleto_vuelo.pdf', 'claims/CLM-A1B2C3D4/boleto_vuelo.pdf', 'AIRLINE: American Airlines\nFLIGHT: AA123\nDATE: 2024-01-15\nPASSENGER: Juan Pérez', 'FLIGHT_TICKET', TRUE),
(1, 1, 'recibo_hotel.pdf', 'application/pdf', 189440, 'https://storage.googleapis.com/bucket/recibo_hotel.pdf', 'claims/CLM-A1B2C3D4/recibo_hotel.pdf', 'HOTEL: Hilton\nROOM: 305\nCHECK-IN: 2024-01-15\nAMOUNT: $150.00', 'HOTEL_RECEIPT', TRUE),
(2, 2, 'comprobante_hotel.pdf', 'application/pdf', 156672, 'https://storage.googleapis.com/bucket/comprobante_hotel.pdf', 'claims/CLM-E5F6G7H8/comprobante_hotel.pdf', 'HOTEL: Marriott\nROOM: 412\nCHECK-IN: 2024-01-20\nAMOUNT: $200.00', 'HOTEL_RECEIPT', TRUE);

-- 4. Insertar actualizaciones de estado
INSERT INTO CLAIM_STATUS_UPDATES (claim_submission_id, old_status, new_status, reason, analyst_name) VALUES
(1, NULL, 'PENDING', 'Claim creado automáticamente desde email', 'Sistema Automático'),
(2, NULL, 'PENDING', 'Claim creado automáticamente desde email', 'Sistema Automático'),
(2, 'PENDING', 'UNDER_REVIEW', 'Documentos recibidos, iniciando revisión', 'Ana López');

-- 5. Actualizar estadísticas del dashboard
UPDATE DASHBOARD_STATS SET 
    total_claims = 2,
    pending_claims = 1,
    approved_claims = 0,
    rejected_claims = 0,
    closed_claims = 0,
    total_amount_requested = 2300.00,
    total_amount_approved = 0.00,
    last_updated = CURRENT_TIMESTAMP;

-- 6. Consultas de validación

-- Verificar emails insertados
SELECT 'EMAILS INSERTADOS' as test_name, COUNT(*) as count FROM emails;

-- Verificar claims insertados
SELECT 'CLAIMS INSERTADOS' as test_name, COUNT(*) as count FROM claim_submissions;

-- Verificar documentos insertados
SELECT 'DOCUMENTOS INSERTADOS' as test_name, COUNT(*) as count FROM documents_agent_ocr;

-- Verificar actualizaciones de estado
SELECT 'ACTUALIZACIONES DE ESTADO' as test_name, COUNT(*) as count FROM claim_status_updates;

-- Verificar estadísticas actualizadas
SELECT 'ESTADÍSTICAS ACTUALIZADAS' as test_name, total_claims, pending_claims, total_amount_requested FROM dashboard_stats;

-- 7. Consultas de prueba de relaciones

-- Emails con sus claims asociados
SELECT 
    e.id as email_id,
    e.subject,
    e.from_email,
    cs.claim_number,
    cs.status,
    cs.estimated_amount
FROM emails e
LEFT JOIN claim_submissions cs ON e.id = cs.email_id
ORDER BY e.id;

-- Claims con sus documentos
SELECT 
    cs.claim_number,
    cs.customer_name,
    cs.claim_type,
    COUNT(d.id) as document_count,
    SUM(d.file_size) as total_size_bytes
FROM claim_submissions cs
LEFT JOIN documents_agent_ocr d ON cs.id = d.claim_submission_id
GROUP BY cs.id, cs.claim_number, cs.customer_name, cs.claim_type
ORDER BY cs.id;

-- Historial de cambios de estado por claim
SELECT 
    cs.claim_number,
    cs.customer_name,
    csu.old_status,
    csu.new_status,
    csu.reason,
    csu.analyst_name,
    csu.created_at
FROM claim_submissions cs
JOIN claim_status_updates csu ON cs.id = csu.claim_submission_id
ORDER BY cs.id, csu.created_at;

-- 8. Limpiar datos de prueba (opcional - ejecutar solo si quieres limpiar)
-- DELETE FROM claim_status_updates;
-- DELETE FROM documents_agent_ocr;
-- DELETE FROM claim_submissions;
-- DELETE FROM emails;
-- UPDATE dashboard_stats SET total_claims = 0, pending_claims = 0, total_amount_requested = 0.00; 