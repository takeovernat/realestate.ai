# Deployment Guide

This guide covers deploying the AI Property Matchmaker to production.

## Architecture Overview

- **Frontend**: Next.js 14 (deployed to Vercel)
- **Backend**: FastAPI Python (deployed to Railway/Render/AWS)
- **Data**: JSON file (included in backend deployment)

## Option 1: Vercel (Frontend) + Railway (Backend)

### Deploy Backend to Railway

1. **Create Railway Account**: https://railway.app

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo" or "Empty Project"

3. **Deploy Backend**
   ```bash
   cd backend
   # Initialize git if needed
   git init
   git add .
   git commit -m "Initial backend commit"
   ```

4. **Configure Railway**
   - Add environment variables (if any)
   - Railway will auto-detect Dockerfile
   - Or use Python buildpack with start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Get Backend URL**
   - Railway provides a URL like: `https://your-app.railway.app`

### Deploy Frontend to Vercel

1. **Prepare for Deployment**
   ```bash
   # Update .env.local with production backend URL
   NEXT_PUBLIC_API_URL=https://your-app.railway.app
   ```

2. **Deploy to Vercel**
   ```bash
   npm install -g vercel
   vercel
   ```

3. **Add Environment Variables in Vercel**
   - Go to Vercel Dashboard → Project → Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_URL` = your Railway backend URL

4. **Redeploy**
   ```bash
   vercel --prod
   ```

## Option 2: Vercel (Frontend) + Render (Backend)

### Deploy Backend to Render

1. **Create Render Account**: https://render.com

2. **Create New Web Service**
   - Connect your GitHub repo
   - Select the backend directory
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Configure**
   - Environment: Python 3
   - Add environment variables if needed

4. **Get Backend URL**
   - Render provides: `https://your-app.onrender.com`

### Deploy Frontend
- Same as Vercel instructions above

## Option 3: Docker Deployment

### Backend (Docker)

```bash
cd backend
docker build -t property-matcher .
docker run -p 8000:8000 property-matcher
```

### Frontend (Docker)

Create `Dockerfile` in root:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

Build and run:
```bash
docker build -t property-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://backend:8000 property-frontend
```

## Option 4: AWS Lambda (Backend) + Vercel (Frontend)

### Backend to AWS Lambda

1. **Install Mangum** (ASGI adapter for Lambda)
   ```bash
   pip install mangum
   ```

2. **Modify `main.py`**
   ```python
   from mangum import Mangum
   
   # At the end of main.py
   handler = Mangum(app)
   ```

3. **Deploy with AWS SAM or Serverless Framework**

## Environment Variables

### Frontend (.env.local or Vercel)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### Backend (if needed)
```
ALLOWED_ORIGINS=https://your-frontend-url.com
```

## Post-Deployment Checklist

- [ ] Backend health check works: `https://backend-url/health`
- [ ] Frontend loads successfully
- [ ] CORS configured correctly
- [ ] API calls work from frontend to backend
- [ ] Environment variables are set
- [ ] SSL/HTTPS enabled on both services

## Monitoring & Logs

### Railway
- View logs in Railway dashboard
- Set up log drains if needed

### Render
- View logs in Render dashboard
- Configure log retention

### Vercel
- View deployment logs and runtime logs in Vercel dashboard

## Scaling Considerations

1. **Backend**: 
   - Railway/Render auto-scale
   - Add Redis for caching if needed
   - Consider load balancer for high traffic

2. **Frontend**:
   - Vercel handles scaling automatically
   - Edge functions for API routes

3. **Database**:
   - Current: JSON file (sufficient for demo)
   - Production: PostgreSQL/MongoDB

## Cost Estimates

- **Vercel**: Free tier suitable for demo/interview
- **Railway**: $5-20/month depending on usage
- **Render**: Free tier available, paid tiers from $7/month

## Troubleshooting

### CORS Issues
Update `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-url.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 404 Errors on Backend
- Ensure backend is running
- Check URL is correct (no trailing slashes)
- Verify environment variables

### Build Failures
- Check Node.js version (use 18+)
- Check Python version (use 3.9+)
- Review build logs carefully
