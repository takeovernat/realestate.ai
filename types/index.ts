// Type definitions for the AI Property Matchmaker application

export interface Home {
  id: number;
  name: string;
  type: 'condo' | 'single-family' | 'townhouse';
  price: number;
  sq_ft: number;
  bedrooms: number;
  bathrooms: number;
  amenities: string[];
  location: string;
  description: string;
}

export interface UserPreferences {
  homeType: string;
  budget: number;
  amenities: string[];
  customNeeds: string;
}

export interface MatchedHome extends Home {
  score: number;
  explanation: string;
}

export interface MatchResponse {
  matches: MatchedHome[];
  message?: string;
}

export interface FormData {
  homeType: string;
  budget: string;
  amenities: string[];
  customNeeds: string;
}
