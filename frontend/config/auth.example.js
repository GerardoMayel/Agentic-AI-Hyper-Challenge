// Authentication configuration example
// Copy this file to auth.js and update with your credentials

export const AUTH_CONFIG = {
  // Demo credentials - In production, these should come from environment variables
  demoCredentials: {
    email: 'your-demo-email@example.com',
    password: 'your-demo-password'
  },
  
  // Session configuration
  sessionTimeout: 24 * 60 * 60 * 1000, // 24 hours in milliseconds
  
  // Redirect paths
  loginPath: '/login',
  dashboardPath: '/dashboard',
  defaultPath: '/'
} 