# Database URL Configuration Guide

## Overview
This project uses different database URLs for different environments:

- **Development (Local)**: External Database URL
- **Production (Render)**: Internal Database URL (automatically configured)

## Configuration

### 1. Local Development (.env file)
Update your `.env` file with the **External Database URL**:

```bash
DATABASE_URL=postgresql://agent:QRp3aBO6eGFT2mXY6p1nTmAxd41QRFJc@dpg-d1k9hmer433s73c9g7mg-a.oregon-postgres.render.com/claims_ropj_z7d1
```

### 2. Production (Render)
The `render.yaml` file is configured to automatically use the **Internal Database URL**:

```yaml
envVars:
  - key: DATABASE_URL
    fromDatabase:
      name: claims-db
      property: connectionString
```

## Database URLs from Render

### External Database URL (for local development)
```
postgresql://agent:QRp3aBO6eGFT2mXY6p1nTmAxd41QRFJc@dpg-d1k9hmer433s73c9g7mg-a.oregon-postgres.render.com/claims_ropj_z7d1
```

### Internal Database URL (for Render services)
This is automatically configured by Render and is faster for services running on Render.

## Testing Connection

### Local Testing
```bash
cd backend
python test_correct_db.py
```

### Production Testing
The connection will be tested automatically when the backend is deployed to Render.

## Environment Variables Required

### Backend (.env for local development)
```bash
DATABASE_URL=postgresql://agent:QRp3aBO6eGFT2mXY6p1nTmAxd41QRFJc@dpg-d1k9hmer433s73c9g7mg-a.oregon-postgres.render.com/claims_ropj_z7d1
GOOGLE_CLOUD_PROJECT_ID=your_project_id
GOOGLE_CLOUD_STORAGE_BUCKET=your_bucket_name
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type": "service_account", ...}
```

### Frontend (.env.local for local development)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Frontend (Render production)
```bash
NEXT_PUBLIC_API_URL=https://zurich-claims-api.onrender.com
```

## Next Steps

1. Update your `.env` file with the External Database URL
2. Deploy the backend to Render
3. Update the frontend's `NEXT_PUBLIC_API_URL` in Render
4. Test the complete integration 