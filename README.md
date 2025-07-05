# Claims Management System

Automated claims management system that processes incoming emails and generates claims automatically.

## 🚀 Features

- **Automatic email processing**: Monitors email `gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com` for emails containing the keyword "claim"
- **Web dashboard**: Web interface to view and manage claims
- **Cloud storage**: Documents stored in Google Cloud Storage
- **PostgreSQL database**: Persistent storage for claims and documents
- **REST API**: Endpoints for integration with other systems
- **Web forms**: Responsive forms to complete claim information

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Gmail API     │    │   Reflex App    │    │   PostgreSQL    │
│   (Email Input) │───▶│   (Web Server)  │───▶│   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Google Cloud    │
                       │ Storage         │
                       │ (Documents)     │
                       └─────────────────┘
```

## 📋 Requirements

- Python 3.11+
- PostgreSQL database
- Google Cloud Storage bucket
- Gmail API credentials
- Gemini API key

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd Agentic-AI-Hyper-Challenge
```

### 2. Install dependencies
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure environment variables
Create `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Google Cloud
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_BUCKET_NAME=your-bucket-name
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type": "service_account", ...}

# Gmail API
GMAIL_CREDENTIALS_JSON={"installed": {"client_id": "...", ...}}
GMAIL_TOKEN_JSON={"token": "...", "refresh_token": "...", ...}

# AI Services
GEMINI_API_KEY=your-gemini-api-key

# Email Services
SENDGRID_API_KEY=your-sendgrid-api-key

# App Configuration
SECRET_KEY=your-secret-key
```

### 4. Configure database
```bash
# Create tables
python create_tables.py

# Or use Alembic for migrations
alembic upgrade head
```

## 🚀 Execution

### Option 1: Using the automated script (Recommended)
```bash
# Make sure the script is executable
chmod +x run_app.sh

# Run the application
./run_app.sh
```

### Option 2: Manual execution
```bash
# Activate virtual environment
source venv/bin/activate

# Run Reflex directly
reflex run

# Or using the Python script
python start_app.py
```

The application will be available at:
- **Dashboard**: http://localhost:3000/dashboard
- **Home**: http://localhost:3000
- **Forms**: http://localhost:3000/claim-form

### Render deployment

1. Connect the repository to Render
2. Configure environment variables in Render
3. The application will deploy automatically

**Production URL**: https://claims-management-system-j7jz.onrender.com

## 📧 Email Processing Flow

1. **Monitoring**: Application checks for new emails every 5 minutes
2. **Detection**: Searches for emails with keyword "claim"
3. **Processing**: Extracts information and attached documents
4. **Storage**: Saves to database and uploads documents to storage
5. **Response**: Sends confirmation email with claim number
6. **Forms**: Provides links to web forms and PDF

## 🔧 API Endpoints

### Email Webhook
```
POST /api/email-webhook
```
Receives incoming emails and processes claims.

### Claims API
```
GET /api/claims
```
Gets list of claims.

```
GET /api/claims/{claim_number}
```
Gets details of a specific claim.

## 🧪 Testing

### Test the application
```bash
python test_complete_flow.py
```

### Test email processing
```bash
python test_claims_email_processing.py
```

## 📊 Dashboard

The web dashboard provides:
- Claims and documents statistics
- Recent claims list
- System status
- Button to manually process emails
- Links to forms and details

## 🔒 Security

- Credentials stored in environment variables
- OAuth2 authentication for Gmail API
- Secure access tokens
- Input data validation

## 📝 Logs

The application logs:
- Email processing
- Errors and exceptions
- System status
- Database activity

## 🚨 Monitoring

- Health check endpoint for monitoring
- Detailed operation logs
- Processing metrics
- External service status

## 📞 Support

For issues or questions:
1. Check application logs
2. Verify environment variable configuration
3. Test individual endpoints
4. Verify connectivity with external services

## 🔄 Updates

To update the application:
1. Pull changes from repository
2. Update dependencies: `pip install -r requirements.txt`
3. Run database migrations if necessary
4. Restart the application

---

**Note**: The application is designed to run continuously and process emails automatically. In production, it's recommended to use a process manager like PM2 or systemd.
