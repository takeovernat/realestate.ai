'use client';

import { MatchedHome } from '@/types';

interface HomeCardProps {
  home: MatchedHome;
}

export default function HomeCard({ home }: HomeCardProps) {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
    }).format(price);
  };

  const formatSquareFeet = (sqFt: number) => {
    return new Intl.NumberFormat('en-US').format(sqFt);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
      {/* Image Placeholder */}
      <div className="relative h-48 bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center">
        <div className="text-white text-center">
          <div className="text-6xl mb-2">🏡</div>
          <p className="text-sm font-medium">{home.location}</p>
        </div>
        {/* Match Score Badge */}
        <div className="absolute top-4 right-4 bg-green-500 text-white px-3 py-1 rounded-full text-sm font-bold">
          {Math.round(home.score * 100)}% Match
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {/* Title and Type */}
        <div className="mb-3">
          <h3 className="text-xl font-bold text-gray-900 mb-1">{home.name}</h3>
          <p className="text-sm text-gray-600 capitalize">{home.type.replace('-', ' ')}</p>
        </div>

        {/* Price and Details */}
        <div className="mb-4">
          <p className="text-2xl font-bold text-blue-600 mb-2">
            {formatPrice(home.price)}
          </p>
          <div className="flex items-center gap-4 text-sm text-gray-600">
            <span>🛏️ {home.bedrooms} beds</span>
            <span>🛁 {home.bathrooms} baths</span>
            <span>📏 {formatSquareFeet(home.sq_ft)} sq ft</span>
          </div>
        </div>

        {/* Amenities */}
        <div className="mb-4">
          <div className="flex flex-wrap gap-2">
            {home.amenities.slice(0, 4).map((amenity) => (
              <span
                key={amenity}
                className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium capitalize"
              >
                {amenity}
              </span>
            ))}
            {home.amenities.length > 4 && (
              <span className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-xs font-medium">
                +{home.amenities.length - 4} more
              </span>
            )}
          </div>
        </div>

        {/* AI Explanation */}
        <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-sm text-gray-700 flex items-start">
            <span className="mr-2 text-lg">✨</span>
            <span>{home.explanation}</span>
          </p>
        </div>

        {/* Description */}
        <p className="text-sm text-gray-600 mb-4 line-clamp-3">
          {home.description}
        </p>

        {/* Contact Button */}
        <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200 active:scale-95">
          Contact Agent
        </button>
      </div>
    </div>
  );
}
