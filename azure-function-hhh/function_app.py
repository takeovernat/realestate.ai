# function_app.py

import azure.functions as func
import logging
import json
from pydantic import BaseModel, ValidationError
from typing import List, Optional, Dict, Any

# Import helper class and data loader from the sibling file
from matcher import PropertyMatcher, load_homes_data 

# Set up logging for the Azure Function host
logger = logging.getLogger('azure.functions')

# --- Pydantic Models (Copied from original main.py) ---
class UserPreferences(BaseModel):
    homeType: str
    budget: int
    amenities: List[str]
    customNeeds: Optional[str] = ""

class HomeBase(BaseModel):
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

class MatchedHome(HomeBase):
    score: float
    explanation: str

class MatchResponse(BaseModel):
    matches: List[MatchedHome]
    message: Optional[str] = None
# --- End Pydantic Models ---


# --- Global Initialization ---
# This code runs once when the function app instance starts (cold start)
HOMES_LOADED = False
HOMES_COUNT = 0
MATCHER = None

try:
    homes_data = load_homes_data()
    MATCHER = PropertyMatcher(homes_data)
    HOMES_COUNT = len(homes_data)
    HOMES_LOADED = True
    logger.info(f"Initialized PropertyMatcher with {HOMES_COUNT} homes.")
except Exception as e:
    logger.error(f"Failed to initialize PropertyMatcher: {e}")

# Initialize the Function App object
app = func.FunctionApp()


# ----------------------------------------------------------------------
# 1. HealthCheck Endpoint (GET /api/health)
# ----------------------------------------------------------------------
@app.route(route="health", methods=["GET"], auth_level=func.AuthLevel.FUNCTION)
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint using the Python V2 model."""
    logger.info('Health check request received.')

    response_data = {
        "status": "healthy", 
        "homes_loaded": HOMES_COUNT,
        "message": "API operational"
    }
    
    status_code = 200
    if not HOMES_LOADED:
        response_data['status'] = 'data_error'
        response_data['message'] = 'API operational but homes data failed to load.'
        status_code = 503

    return func.HttpResponse(
        json.dumps(response_data),
        mimetype="application/json",
        status_code=status_code
    )


# ----------------------------------------------------------------------
# 2. MatchProperties Endpoint (POST /api/match)
# ----------------------------------------------------------------------
@app.route(route="match", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def match_properties(req: func.HttpRequest) -> func.HttpResponse:
    """Property matching endpoint using the Python V2 model."""
    logger.info('Property match request received.')

    # 1. Check Initialization
    if not HOMES_LOADED or MATCHER is None:
        return func.HttpResponse(
             json.dumps({"error": "Service unavailable: Matcher not initialized.", "matches": []}),
             mimetype="application/json",
             status_code=503
        )
        
    # 2. Get Request Body
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Please pass a valid JSON payload.", status_code=400)

    # 3. Validate Request Body with Pydantic
    try:
        preferences = UserPreferences(**req_body)
    except ValidationError as e:
        logger.warning(f"Validation Error: {e.errors()}")
        return func.HttpResponse(
             json.dumps({"error": "Invalid request format", "details": e.errors()}),
             mimetype="application/json",
             status_code=400
        )

    # 4. Process Request
    try:
        # Use the PropertyMatcher to find and rank homes
        matched_homes_raw: List[Dict[str, Any]] = MATCHER.find_matches(
            home_type=preferences.homeType,
            budget=preferences.budget,
            amenities=preferences.amenities,
            custom_needs=preferences.customNeeds
        )
        
        # Convert to Pydantic objects for clean output
        results = [MatchedHome(**home) for home in matched_homes_raw]
        
        message = None
        if not results:
            message = "No properties found matching your criteria. Try adjusting your preferences."

        response = MatchResponse(matches=results, message=message)
        
        # 5. Return Response
        return func.HttpResponse(
            # Pydantic's method for reliable JSON serialization
            response.model_dump_json(by_alias=True, indent=2), 
            mimetype="application/json",
            status_code=200
        )
    
    except Exception as e:
        logger.error(f"Internal processing error: {e}", exc_info=True)
        return func.HttpResponse(
             json.dumps({"error": "Internal server error during property matching.", "details": str(e)}),
             mimetype="application/json",
             status_code=500
        )