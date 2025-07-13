-- Script SQL para validar que las tablas del sistema de emails se crearon correctamente
-- Ejecutar en pgAdmin o psql después de crear las tablas

-- 1. Verificar que todas las tablas existen
SELECT 
    table_name,
    CASE 
        WHEN table_name IN ('emails', 'claim_submissions', 'documents_agent_ocr', 'claim_status_updates', 'dashboard_stats') 
        THEN '✅ EXISTE' 
        ELSE '❌ FALTANTE' 
    END as status
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('emails', 'claim_submissions', 'documents_agent_ocr', 'claim_status_updates', 'dashboard_stats')
ORDER BY table_name;

-- 2. Verificar estructura de la tabla EMAILS
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default,
    CASE 
        WHEN column_name IN ('id', 'gmail_id', 'thread_id', 'from_email', 'to_email', 'subject') 
        THEN '✅ REQUERIDO' 
        ELSE '✅ OPCIONAL' 
    END as validation
FROM information_schema.columns 
WHERE table_name = 'emails' 
ORDER BY ordinal_position;

-- 3. Verificar estructura de la tabla CLAIM_SUBMISSIONS
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default,
    CASE 
        WHEN column_name IN ('id', 'claim_number', 'email_id', 'customer_name', 'customer_email', 'claim_type') 
        THEN '✅ REQUERIDO' 
        ELSE '✅ OPCIONAL' 
    END as validation
FROM information_schema.columns 
WHERE table_name = 'claim_submissions' 
ORDER BY ordinal_position;

-- 4. Verificar estructura de la tabla DOCUMENTS_AGENT_OCR
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default,
    CASE 
        WHEN column_name IN ('id', 'claim_submission_id', 'original_filename', 'file_type', 'file_size', 'storage_url', 'storage_path') 
        THEN '✅ REQUERIDO' 
        ELSE '✅ OPCIONAL' 
    END as validation
FROM information_schema.columns 
WHERE table_name = 'documents_agent_ocr' 
ORDER BY ordinal_position;

-- 5. Verificar estructura de la tabla CLAIM_STATUS_UPDATES
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default,
    CASE 
        WHEN column_name IN ('id', 'claim_submission_id', 'new_status') 
        THEN '✅ REQUERIDO' 
        ELSE '✅ OPCIONAL' 
    END as validation
FROM information_schema.columns 
WHERE table_name = 'claim_status_updates' 
ORDER BY ordinal_position;

-- 6. Verificar estructura de la tabla DASHBOARD_STATS
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default,
    CASE 
        WHEN column_name = 'id' 
        THEN '✅ REQUERIDO' 
        ELSE '✅ OPCIONAL' 
    END as validation
FROM information_schema.columns 
WHERE table_name = 'dashboard_stats' 
ORDER BY ordinal_position;

-- 7. Verificar que las foreign keys existen
SELECT 
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name,
    '✅ FK EXISTE' as status
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY' 
AND tc.table_name IN ('claim_submissions', 'documents_agent_ocr', 'claim_status_updates')
ORDER BY tc.table_name, kcu.column_name;

-- 8. Verificar que los índices existen
SELECT 
    indexname,
    tablename,
    indexdef,
    '✅ ÍNDICE EXISTE' as status
FROM pg_indexes 
WHERE tablename IN ('emails', 'claim_submissions', 'documents_agent_ocr', 'claim_status_updates')
AND indexname LIKE 'idx_%'
ORDER BY tablename, indexname;

-- 9. Verificar que el registro inicial existe en DASHBOARD_STATS
SELECT 
    total_claims,
    pending_claims,
    approved_claims,
    rejected_claims,
    closed_claims,
    total_amount_requested,
    total_amount_approved,
    CASE 
        WHEN total_claims = 0 AND pending_claims = 0 THEN '✅ REGISTRO INICIAL CORRECTO'
        ELSE '⚠️ REGISTRO INICIAL MODIFICADO'
    END as validation
FROM dashboard_stats 
LIMIT 1;

-- 10. Resumen de validación
SELECT 
    'RESUMEN DE VALIDACIÓN' as summary,
    COUNT(*) as total_tables,
    COUNT(CASE WHEN table_name IS NOT NULL THEN 1 END) as tables_found,
    CASE 
        WHEN COUNT(*) = 5 THEN '✅ TODAS LAS TABLAS EXISTEN'
        ELSE '❌ FALTAN TABLAS'
    END as status
FROM (
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name IN ('emails', 'claim_submissions', 'documents_agent_ocr', 'claim_status_updates', 'dashboard_stats')
) as table_check; 