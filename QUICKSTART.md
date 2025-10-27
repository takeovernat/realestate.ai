# Quick Start Guide

## Setup (First Time)

1. **Install Frontend Dependencies**
   ```bash
   npm install
   ```

2. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   # or with --break-system-packages if needed:
   pip install -r requirements.txt --break-system-packages
   cd ..
   ```

3. **Create Environment File** (optional)
   ```bash
   cp .env.example .env.local
   ```

## Running the App

**You need TWO terminal windows:**

### Terminal 1 - Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend
```bash
npm run dev
```

## Access the App

Open your browser to: **http://localhost:3000**

## Testing the API Directly

```bash
curl -X POST http://localhost:8000/match \
  -H "Content-Type: application/json" \
  -d '{
    "homeType": "single-family",
    "budget": 500000,
    "amenities": ["pool", "park"],
    "customNeeds": "Need a home office and large backyard"
  }'
```

## Troubleshooting

### Port Already in Use
- Frontend (3000): Kill the process or change port in `package.json`
- Backend (8000): Kill the process or change port in startup command

### CORS Errors
- Make sure backend is running on port 8000
- Check CORS settings in `backend/main.py`

### Module Not Found
- Run `npm install` again
- For Python: ensure you're in the `backend` directory when installing packages

## Project Structure
```
ai-property-matchmaker/
├── app/                    # Next.js pages and API routes
├── components/             # React components
├── backend/                # FastAPI Python backend
├── data/                   # Sample property data
└── types/                  # TypeScript definitions
```
