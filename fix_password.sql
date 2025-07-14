-- Check current credentials
SELECT email, password_hash, role, is_active FROM auth_credentials;

-- Update password to the correct one (ZurichDemo2024!)
UPDATE auth_credentials 
SET password_hash = 'ZurichDemo2024!', 
    updated_at = CURRENT_TIMESTAMP 
WHERE email = 'analyst@zurich-demo.com';

-- Verify the update
SELECT email, password_hash, role, is_active FROM auth_credentials; 