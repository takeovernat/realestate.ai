# AI Property Matchmaker

An intelligent property matching system for master-planned communities, built with Next.js 14 and FastAPI. This application helps users find their dream home by matching their preferences with available properties using AI-driven recommendations.

## 🏡 About

The AI Property Matchmaker is designed for modern master-planned communities like The Woodlands, TX. It uses advanced matching algorithms to connect homebuyers with properties that best fit their lifestyle, budget, and amenity preferences.

## 🚀 Features

- **Smart Matching**: AI-powered property recommendations based on user preferences
- **Interactive Form**: Easy-to-use interface for specifying home requirements
- **Real-time Results**: Instant property matches with detailed explanations
- **Responsive Design**: Beautiful, mobile-friendly interface built with Tailwind CSS
- **Full-Stack Architecture**: Next.js frontend with FastAPI backend

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Git

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ai-property-matchmaker
```

### 2. Install Frontend Dependencies

```bash
npm install
```

### 3. Install Backend Dependencies

```bash
cd backend
pip install fastapi uvicorn python-multipart scikit-learn numpy
cd ..
```

## 🏃 Running the Application

You'll need to run both the frontend and backend servers:

### Terminal 1: Start the FastAPI Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`

### Terminal 2: Start the Next.js Frontend

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
ai-property-matchmaker/
├── app/
│   ├── api/
│   │   └── match/
│   │       └── route.ts          # API route to communicate with FastAPI
│   ├── layout.tsx                 # Root layout with metadata
│   └── page.tsx                   # Main page component
├── components/
│   ├── HomeCard.tsx               # Property card component
│   ├── PreferenceForm.tsx         # User preference form
│   └── ResultsGrid.tsx            # Grid layout for results
├── backend/
│   ├── main.py                    # FastAPI application
│   └── matcher.py                 # AI matching logic
├── data/
│   └── homes.json                 # Sample property data
├── public/                        # Static assets
├── types/
│   └── index.ts                   # TypeScript type definitions
├── package.json
├── tsconfig.json
└── README.md
```

## 🎯 How It Works

### Frontend (Next.js)

1. User fills out the preference form with budget, home type, amenities, and custom needs
2. Form data is sent to the Next.js API route (`/api/match`)
3. Results are displayed in an attractive card-based grid

### Backend (FastAPI)

1. Receives user preferences via POST request to `/match` endpoint
2. Uses text embedding and cosine similarity to match preferences with properties
3. Ranks properties based on multiple factors (budget, amenities, custom needs)
4. Returns top 3 matches with AI-generated explanations

### Mock AI Logic

The backend simulates LLM integration using:

- **TF-IDF Vectorization**: Converts text descriptions to numerical vectors
- **Cosine Similarity**: Measures similarity between user needs and property features
- **Multi-factor Scoring**: Combines budget matching, amenity overlap, and text similarity
- **Explanation Generation**: Creates natural language explanations for each match

## 🌐 Deployment

### Frontend (Vercel)

```bash
npm run build
# Deploy to Vercel via GitHub integration or Vercel CLI
```

### Backend (Options)

1. **Railway/Render**: Simple Python deployment
2. **AWS Lambda**: Serverless FastAPI with Mangum adapter
3. **Docker**: Containerized deployment
   ```bash
   cd backend
   docker build -t property-matcher .
   docker run -p 8000:8000 property-matcher
   ```

## 🔧 Environment Variables

Create a `.env.local` file in the root directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production, update this to your deployed backend URL.

## 🎨 Customization

### Adding New Properties

Edit `data/homes.json` to add or modify properties:

```json
{
  "id": 11,
  "name": "Your New Home",
  "type": "single-family",
  "price": 500000,
  "sq_ft": 2500,
  "bedrooms": 4,
  "bathrooms": 3,
  "amenities": ["pool", "park", "gym"],
  "location": "Your Location",
  "description": "Description of the property"
}
```

### Styling

Modify Tailwind classes in components or update `tailwind.config.ts` for theme customization.

## 🧪 Testing

```bash
# Test the backend endpoint
curl -X POST http://localhost:8000/match \
  -H "Content-Type: application/json" \
  -d '{
    "homeType": "single-family",
    "budget": 500000,
    "amenities": ["pool", "park"],
    "customNeeds": "Need a home office and large backyard"
  }'
```
