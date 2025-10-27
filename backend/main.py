"""
FastAPI Backend for AI Property Matchmaker
Handles property matching requests using mock AI/LLM logic
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from matcher import PropertyMatcher

# Initialize FastAPI app
app = FastAPI(
    title="AI Property Matchmaker API",
    description="Backend API for intelligent property matching",
    version="1.0.0"
)

# Configure CORS to allow Next.js frontend to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class UserPreferences(BaseModel):
    homeType: str
    budget: int
    amenities: List[str]
    customNeeds: Optional[str] = ""

class Home(BaseModel):
    id: int
    name: str
    type: str
    price: int
    sq_ft: int
    bedrooms: int
    bathrooms: float
    amenities: List[str]
    location: str
    description: str

class MatchedHome(Home):
    score: float
    explanation: str

class MatchResponse(BaseModel):
    matches: List[MatchedHome]
    message: Optional[str] = None

# Load homes data from JSON file
def load_homes_data():
    """Load property data from homes.json file"""
    # Get the path to the data directory (one level up from backend)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '..', 'data', 'homes.json')
    
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to relative path if absolute path fails
        try:
            with open('../data/homes.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception("Could not find homes.json file")

# Initialize the property matcher
homes_data = load_homes_data()
matcher = PropertyMatcher(homes_data)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Property Matchmaker API",
        "version": "1.0.0",
        "endpoints": {
            "/match": "POST - Match properties based on user preferences",
            "/health": "GET - Health check endpoint"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "homes_loaded": len(homes_data)}

@app.post("/match", response_model=MatchResponse)
async def match_properties(preferences: UserPreferences):
    """
    Match properties based on user preferences
    
    This endpoint uses a mock AI/LLM system that:
    1. Scores properties based on budget matching
    2. Evaluates amenity overlap
    3. Uses text similarity for custom needs
    4. Generates natural language explanations
    
    Returns top 3 matching properties
    """
    try:
        # Use the PropertyMatcher to find and rank homes
        matched_homes = matcher.find_matches(
            home_type=preferences.homeType,
            budget=preferences.budget,
            amenities=preferences.amenities,
            custom_needs=preferences.customNeeds
        )
        
        # Convert to MatchedHome objects
        results = []
        for home in matched_homes:
            matched_home = MatchedHome(
                id=home['id'],
                name=home['name'],
                type=home['type'],
                price=home['price'],
                sq_ft=home['sq_ft'],
                bedrooms=home['bedrooms'],
                bathrooms=home['bathrooms'],
                amenities=home['amenities'],
                location=home['location'],
                description=home['description'],
                score=home['score'],
                explanation=home['explanation']
            )
            results.append(matched_home)
        
        message = None
        if len(results) == 0:
            message = "No properties found matching your criteria. Try adjusting your preferences."
        
        return MatchResponse(matches=results, message=message)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)