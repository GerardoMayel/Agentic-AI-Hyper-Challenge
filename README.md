# Claims Management System - Agentic AI

An MVP (Minimum Viable Product) of an intelligent claims management system that processes incoming emails and automates workflows using Google Gemini.

## 🚀 Features

- **Automatic Claims Ingestion**: Receives emails and creates claims automatically
- **Intelligent Extraction**: Uses AI to extract policy numbers and generate summaries
- **Complete Claims Management**: Status tracking, analyst assignment
- **Automatic Communication**: Sends acknowledgments and updates
- **Analyst Dashboard**: Interface to manage claims and configurations
- **Cloud Storage**: Cloudflare R2 for files and PostgreSQL for data
- **Automatic Deployment**: Configured for Render

## 🛠️ Tech Stack

- **Web Framework**: Reflex (Python)
- **Database**: PostgreSQL with SQLAlchemy
- **AI Model**: Google Gemini
- **Email**: SendGrid
- **Storage**: Cloudflare R2
- **Deployment**: Render
- **Migrations**: Alembic

## 📁 Project Structure

```
Agentic-AI-Hyper-Challenge/
├── app/
│   ├── components/          # Reusable components
│   ├── core/               # Application core
│   │   ├── database.py     # Database configuration
│   │   ├── models.py       # SQLAlchemy models (Claims, Policies, etc.)
│   │   ├── crud.py         # CRUD operations
│   │   └── init_db.py      # Database initialization
│   ├── pages/              # Application pages
│   ├── services/           # External services
│   ├── state/              # Reflex states
│   ├── web/api/            # API endpoints
│   └── app.py              # Main application
├── assets/                 # Static files
├── alembic/                # Database migrations
├── alembic.ini            # Migration configuration
├── env.example            # Environment variables example
├── manage_db.py           # Database management script
├── render.yaml            # Render configuration
├── requirements.txt       # Python dependencies
└── rxconfig.py           # Reflex configuration
```

## 🗄️ Data Model

### Main Entities

- **Users**: Analysts and system administrators
- **Policies**: Customer insurance policies
- **Coverages**: Specific coverages for each policy
- **Claims**: Claims reported by customers
- **Documents**: Documents attached to claims
- **ClaimForms**: Claim forms (web or PDF)
- **Communications**: Communication history

### Claim Statuses

- `OPEN_NOTIFIED`: Claim just notified
- `PENDING_CUSTOMER_DOCUMENTS`: Waiting for customer documents
- `UNDER_AI_REVIEW`: Under AI review
- `PENDING_ANALYST_REVIEW`: Pending analyst review
- `ADDITIONAL_INFO_REQUESTED`: Additional information requested
- `DECISION_APPROVED`: Decision approved
- `DECISION_REJECTED`: Decision rejected
- `CLOSED_PAID`: Closed and paid
- `CLOSED_REJECTED`: Closed and rejected
- `IN_LITIGATION`: In litigation

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository>
cd Agentic-AI-Hyper-Challenge
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp env.example .env
```

Edit the `.env` file with your credentials:

```env
# PostgreSQL Database
DATABASE_URL=postgresql://user:password@host:port/dbname

# External Services
GEMINI_API_KEY=your_gemini_api_key
SENDGRID_API_KEY=your_sendgrid_api_key

# Cloudflare R2
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=your_bucket_name
R2_PUBLIC_URL=https://your-public-url.r2.dev

# App Configuration
APP_SECRET_KEY=your_secret_key
ENVIRONMENT=development
FROM_EMAIL=noreply@your-domain.com
```

### 5. Configure database

#### Option A: Using the management script (Recommended)

```bash
# Test database connection
python manage_db.py test

# Initialize database with tables and sample data
python manage_db.py init

# Run migrations (if using Alembic)
python manage_db.py migrate
```

#### Option B: Manual configuration

```bash
# Initialize Alembic
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 6. Run the application

```bash
reflex run
```

The application will be available at `http://localhost:3000`

## 🗄️ Database Management

### Management Script

The project includes a utility script to manage the database:

```bash
# Show help
python manage_db.py help

# Test connection
python manage_db.py test

# Initialize database
python manage_db.py init

# Reset database (WARNING!)
python manage_db.py reset

# Run migrations
python manage_db.py migrate

# Create new migration
python manage_db.py create-migration "Migration description"

# Create test claim
python manage_db.py test-claim

# Show statistics
python manage_db.py stats
```

### Database Structure

#### Main Tables:

- **users**: Analysts and administrators
- **policies**: Insurance policies
- **coverages**: Policy coverages
- **claims**: Reported claims
- **documents**: Attached documents
- **claim_forms**: Claim forms
- **communications**: Communication history

#### Available CRUD Operations:

```python
# Users
crud.get_user_by_username(db, username)
crud.create_user(db, username, hashed_password, role)

# Policies
crud.get_policy_by_number(db, policy_number)
crud.create_policy(db, policy_number, customer_email, ...)

# Claims
crud.create_claim(db, policy)
crud.update_claim_status(db, claim_id, status)
crud.assign_claim_to_analyst(db, claim_id, analyst_id)

# Communications
crud.log_communication(db, claim_id, channel, content, ...)
```

## 📧 SendGrid Configuration

### 1. Configure Webhook

In your SendGrid account:

1. Go to Settings > Mail Settings > Inbound Parse
2. Configure the webhook to point to: `https://your-app.onrender.com/api/email-webhook`
3. Select POST as method
4. Save configuration

### 2. Configure DNS

Configure your domain's MX records to point to SendGrid.

## 🗄️ Database Configuration

### Local PostgreSQL

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb agentic_db
sudo -u postgres createuser agentic_user
sudo -u postgres psql -c "ALTER USER agentic_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE agentic_db TO agentic_user;"
```

### PostgreSQL on Render

1. Create a new PostgreSQL database in Render
2. Copy the connection URL
3. Update `DATABASE_URL` in environment variables

## ☁️ Cloudflare R2 Configuration

1. Create a Cloudflare account
2. Go to R2 Object Storage
3. Create a bucket
4. Generate API tokens
5. Configure the corresponding environment variables

## 🚀 Deployment on Render

### 1. Connect repository

1. Go to Render Dashboard
2. Create a new Web Service
3. Connect your GitHub repository

### 2. Configure environment variables

In Render, configure all necessary environment variables:

- `DATABASE_URL`
- `GEMINI_API_KEY`
- `SENDGRID_API_KEY`
- `R2_ACCOUNT_ID`
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_BUCKET_NAME`
- `R2_PUBLIC_URL`
- `FROM_EMAIL`

### 3. Configure build and start commands

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `reflex run --env prod --app app.app:app --host 0.0.0.0 --port 8000`

## 🔧 Development

### Key File Structure

- `app/app.py`: Application entry point
- `app/core/database.py`: Centralized database configuration
- `app/core/models.py`: Database models (Claims, Policies, etc.)
- `app/core/crud.py`: CRUD operations
- `app/services/`: External API services
- `app/web/api/email_webhook.py`: Claims ingestion endpoint
- `app/pages/`: User interface pages

### Useful Commands

```bash
# Run in development mode
reflex run

# Build for production
reflex export

# Database management
python manage_db.py test
python manage_db.py init
python manage_db.py migrate
python manage_db.py stats

# Run migrations manually
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Change description"
```

### Implemented Design Patterns

- **Dependency Injection**: FastAPI provides database sessions automatically
- **Separation of Concerns**: CRUD separated from endpoints
- **Centralized Configuration**: Database configured in one place
- **Transaction Management**: Sessions closed automatically

## 📝 API Endpoints

### POST /api/email-webhook

Receives incoming emails from SendGrid and creates claims automatically.

**Required Headers:**
- `X-Twilio-Email-Event-Webhook-Signature`
- `X-Twilio-Email-Event-Webhook-Timestamp`

**Body:** Multipart form data with:
- `from`: Sender email
- `to`: Recipient email
- `subject`: Email subject
- `text`: Plain text content
- `html`: HTML content (optional)

**Response:**
```json
{
  "status": "success",
  "message": "Claim processed successfully",
  "claim_number": "CLAIM-20241201123456-123",
  "policy_number": "POL-TRAVEL-2024-001",
  "acknowledgement_sent": true
}
```

## 🔄 Workflow

### 1. Claims Ingestion

1. Customer sends email to `claims@your-domain.com`
2. SendGrid receives email and sends webhook to application
3. System extracts policy number using AI and regex
4. Policy is searched in database
5. Claim is automatically created
6. AI summary of incident is generated
7. Acknowledgment is sent to customer
8. All communication is logged

### 2. Claims Processing

1. **Initial State**: `OPEN_NOTIFIED`
2. **AI Review**: `UNDER_AI_REVIEW` (automatic analysis)
3. **Analyst Review**: `PENDING_ANALYST_REVIEW`
4. **Document Request**: `PENDING_CUSTOMER_DOCUMENTS` (if needed)
5. **Decision**: `DECISION_APPROVED` or `DECISION_REJECTED`
6. **Closure**: `CLOSED_PAID` or `CLOSED_REJECTED`

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is under the MIT License. See the `LICENSE` file for more details.

## 🆘 Support

If you have problems or questions:

1. Check Reflex documentation: https://reflex.dev/
2. Verify environment variable configuration
3. Use the database management script to diagnose issues
4. Check application logs
5. Open an issue in the repository

## 🔮 Upcoming Features

- [ ] Complete analyst dashboard
- [ ] Customer web portal
- [ ] Document upload via email
- [ ] Automatic document analysis
- [ ] Push notification system
- [ ] Complete REST API
- [ ] Automated tests
- [ ] Conversation caching
- [ ] Advanced role and permission system
- [ ] External system integration
- [ ] Reports and analytics
- [ ] Real-time chat for analysts
