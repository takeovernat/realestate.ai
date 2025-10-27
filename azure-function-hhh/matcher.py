"""
Property Matcher Module - Real Claude API Integration
This module uses Anthropic's Claude API for intelligent property matching
with natural language understanding and explanation generation.
"""

import anthropic
import os
import json
import logging
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PropertyMatcher:
    # ... (rest of the class remains largely the same)
    
    def __init__(self, homes_data: List[Dict[str, Any]]):
        """
        Initialize the matcher with property data and Claude client
        """
        self.homes = homes_data
        
        # Initialize Anthropic client
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            logger.error(
                "ANTHROPIC_API_KEY environment variable not set. "
                "Get your API key from https://console.anthropic.com/"
            )
            # Raise a specific error for better logging/handling
            raise EnvironmentError("ANTHROPIC_API_KEY is not set.")
        
        # Use httpx's default timeout (5.0s) or set one explicitly for serverless
        # self.client = anthropic.Anthropic(api_key=api_key, timeout=30.0) 
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def find_matches(
        self, 
        home_type: str, 
        budget: int, 
        amenities: List[str], 
        custom_needs: str
    ) -> List[Dict[str, Any]]:
        # ... (implementation remains the same)
        # Filter properties by type and budget first
        filtered_homes = self._filter_homes(home_type, budget)
        
        if not filtered_homes:
            return []
        
        # Use Claude to evaluate and rank properties
        matches = self._evaluate_with_claude(
            filtered_homes, 
            home_type, 
            budget, 
            amenities, 
            custom_needs
        )
        
        return matches[:3]  # Return top 3
        
    def _filter_homes(self, home_type: str, budget: int) -> List[Dict[str, Any]]:
        # ... (implementation remains the same)
        """
        Pre-filter properties by type and budget
        """
        filtered = []
        
        for home in self.homes:
            # Filter by type
            if home_type != 'any' and home['type'] != home_type:
                continue
            
            # Filter by budget
            if home['price'] > budget:
                continue
            
            filtered.append(home)
        
        return filtered
        
    def _evaluate_with_claude(
        self,
        homes: List[Dict[str, Any]],
        home_type: str,
        budget: int,
        amenities: List[str],
        custom_needs: str
    ) -> List[Dict[str, Any]]:
    
        # Prepare the prompt for Claude
        prompt = self._build_evaluation_prompt(
            homes, home_type, budget, amenities, custom_needs
        )
        try:
            # Call Claude API
            message = self.client.messages.create(
                model="claude-sonnet-4-5", # Updated to current recommended Sonnet model name
                max_tokens=2000,
                temperature=0.3, 
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            # Parse Claude's response
            response_text = message.content[0].text
            matches = self._parse_claude_response(response_text, homes)
            
            return matches
            
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            # Fallback to simple scoring if API fails
            return self._fallback_scoring(homes, budget, amenities, custom_needs)
    
            
            # ... (rest of the try block)
            
        except Exception as e:
            logger.error(f"Error calling Claude API: {e}")
            # Fallback to simple scoring if API fails
            return self._fallback_scoring(homes, budget, amenities, custom_needs)
    
    def _build_evaluation_prompt(
        self,
        homes: List[Dict[str, Any]],
        home_type: str,
        budget: int,
        amenities: List[str],
        custom_needs: str
    ) -> str:
        # ... (implementation remains the same)
        amenities_str = ", ".join(amenities) if amenities else "none specified"
        custom_needs_str = custom_needs if custom_needs.strip() else "none specified"
        
        # Format homes data
        homes_json = json.dumps(homes, indent=2)
        
        prompt = f"""You are a real estate AI assistant helping match homebuyers with properties.

USER PREFERENCES:
- Property Type: {home_type}
- Maximum Budget: ${budget:,}
- Desired Amenities: {amenities_str}
- Custom Needs: {custom_needs_str}

AVAILABLE PROPERTIES:
{homes_json}

TASK:
Evaluate each property and provide a match score from 0.0 to 1.0 based on how well it fits the user's preferences. Consider:

1. **Budget Fit** (30% weight): How well does the price match the budget?
   - Properties at 70-90% of budget are ideal
   - Too cheap might indicate quality concerns
   - Close to budget limit is good

2. **Amenities Match** (40% weight): How many desired amenities does it have?
   - Each matching amenity increases the score
   - Extra amenities are a bonus

3. **Custom Needs** (30% weight): How well does it address specific requirements?
   - Look for semantic matches, not just keywords
   - Consider lifestyle fit and practical needs

RESPONSE FORMAT (important - respond ONLY with valid JSON):
Return a JSON array with the top 3 properties, each with:
{{
  "id": <property_id>,
  "score": <0.0-1.0>,
  "explanation": "<brief, natural explanation 1-2 sentences explaining why this property matches>"
}}

Example:
[
  {{
    "id": 1,
    "score": 0.89,
    "explanation": "This home is perfectly priced at $485,000 within your budget, features your desired pool and park amenities, and has a spacious backyard ideal for your outdoor needs."
  }}
]

Return ONLY the JSON array, no other text. Rank by best matches first."""

        return prompt

    def _parse_claude_response(
        self, 
        response_text: str, 
        homes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        # ... (implementation remains the same)
        try:
            # Extract JSON from response
            # Claude might add text before/after JSON, so find the JSON array
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")
            
            json_str = response_text[start_idx:end_idx]
            evaluations = json.loads(json_str)
            
            # Create a dict for quick home lookup
            homes_dict = {home['id']: home for home in homes}
            
            # Merge evaluations with full home data
            matches = []
            for eval_item in evaluations:
                home_id = eval_item['id']
                if home_id in homes_dict:
                    home = homes_dict[home_id].copy()
                    home['score'] = eval_item['score']
                    home['explanation'] = eval_item['explanation']
                    matches.append(home)
            
            return matches
            
        except Exception as e:
            print(f"Error parsing Claude response: {e}")
            print(f"Response was: {response_text}")
            # Return fallback if parsing fails
            return self._fallback_scoring(homes, 0, [], "")
        
    def _fallback_scoring(
        self,
        homes: List[Dict[str, Any]],
        budget: int,
        amenities: List[str],
        custom_needs: str
    ) -> List[Dict[str, Any]]:
        # ... (implementation remains the same)
        scored_homes = []
        
        for home in homes:
            # Simple scoring logic
            score = 0.5  # Base score
            
            # Budget factor
            if budget > 0:
                price_ratio = home['price'] / budget
                if 0.7 <= price_ratio <= 0.9:
                    score += 0.2
                elif price_ratio < 0.7:
                    score += 0.1
            
            # Amenity factor
            if amenities:
                home_amenities = set(home.get('amenities', []))
                desired = set(amenities)
                overlap = len(home_amenities & desired)
                score += (overlap / len(desired)) * 0.3
            
            home_copy = home.copy()
            home_copy['score'] = round(score, 3)
            home_copy['explanation'] = f"This {home['type']} home at ${home['price']:,} offers {home['bedrooms']} bedrooms and {home['bathrooms']} bathrooms in {home['location']}."
            
            scored_homes.append(home_copy)
        
        # Sort by score descending
        scored_homes.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_homes
        
# --- Global utility function for data loading ---

def load_homes_data():
    """Load property data from homes.json file, designed for serverless environment"""
    
    # Path strategy: Look for 'data/homes.json' relative to the Function App root
    # Azure Functions often runs from the project root or the function directory.
    # The 'data' folder should be a sibling to the function folders.
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check for the structure where 'data' is a sibling folder
    data_path = os.path.join(base_dir, '..', 'data', 'homes.json')
    
    if not os.path.exists(data_path):
        # Fallback for local testing or different deployment structure
        data_path = os.path.join(base_dir, 'data', 'homes.json')
        if not os.path.exists(data_path):
             data_path = 'homes.json' # Try root-level 
    
    try:
        with open(data_path, 'r') as f:
            logger.info(f"Successfully loaded homes data from: {data_path}")
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Could not find homes.json file at: {data_path}")
        raise FileNotFoundError(f"Could not find homes.json file at any expected location.")
    except Exception as e:
        logger.error(f"Error loading homes data: {e}")
        raise Exception(f"Error loading homes data: {e}")