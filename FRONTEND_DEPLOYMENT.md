# Frontend Deployment Guide

## Current Status: Frontend Only

This deployment is for the **frontend static site only**. The backend will be deployed separately later.

## Local Testing

### 1. Development Mode
```bash
cd frontend
npm run dev
```
Access: http://localhost:3000

### 2. Static Build Testing
```bash
cd frontend
npm run build
cd out
python3 -m http.server 3000
```
Access: http://localhost:3000

## Render Deployment

### 1. Create New Static Site in Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Static Site"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `zurich-claims-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/out`
   - **Environment**: Production

### 2. Environment Variables

For now, no environment variables are needed since we're not connecting to a backend yet.

### 3. Custom Domain (Optional)

You can add a custom domain later if needed.

## File Structure

```
frontend/
├── pages/           # Next.js pages
├── styles/          # CSS styles
├── out/             # Static build output (generated)
├── package.json     # Dependencies
└── next.config.js   # Next.js configuration
```

## Next Steps

1. ✅ Deploy frontend static site
2. 🔄 Test all pages work correctly
3. 🔄 Deploy backend API
4. 🔄 Connect frontend to backend
5. 🔄 Add environment variables for API URL

## Troubleshooting

- If build fails, check Node.js version (should be 18+)
- If pages don't load, verify the `out/` directory contains HTML files
- If styles don't load, check Tailwind CSS compilation 