'use client';

import { useState } from 'react';
import { FormData } from '@/types';

interface PreferenceFormProps {
  onSubmit: (data: FormData) => void;
  loading: boolean;
}

export default function PreferenceForm({ onSubmit, loading }: PreferenceFormProps) {
  const [formData, setFormData] = useState<FormData>({
    homeType: '',
    budget: '',
    amenities: [],
    customNeeds: '',
  });

  const availableAmenities = [
    'pool',
    'gym',
    'park',
    'garage',
    'playground',
    'lake',
    'golf',
    'spa',
    'clubhouse',
    'trails',
  ];

  const handleAmenityToggle = (amenity: string) => {
    setFormData((prev) => ({
      ...prev,
      amenities: prev.amenities.includes(amenity)
        ? prev.amenities.filter((a) => a !== amenity)
        : [...prev.amenities, amenity],
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Home Type */}
      <div>
        <label htmlFor="homeType" className="block text-sm font-medium text-gray-700 mb-2">
          Property Type
        </label>
        <select
          id="homeType"
          value={formData.homeType}
          onChange={(e) => setFormData({ ...formData, homeType: e.target.value })}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          required
        >
          <option value="">Select a property type</option>
          <option value="single-family">Single Family Home</option>
          <option value="condo">Condo</option>
          <option value="townhouse">Townhouse</option>
          <option value="any">Any Type</option>
        </select>
      </div>

      {/* Budget */}
      <div>
        <label htmlFor="budget" className="block text-sm font-medium text-gray-700 mb-2">
          Maximum Budget
        </label>
        <div className="relative">
          <span className="absolute left-4 top-2 text-gray-500">$</span>
          <input
            type="number"
            id="budget"
            value={formData.budget}
            onChange={(e) => setFormData({ ...formData, budget: e.target.value })}
            placeholder="500000"
            min="0"
            step="1000"
            className="w-full pl-8 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
        </div>
        <p className="mt-1 text-sm text-gray-500">
          Enter your maximum home budget
        </p>
      </div>

      {/* Amenities */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Desired Amenities
        </label>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
          {availableAmenities.map((amenity) => (
            <label
              key={amenity}
              className={`flex items-center justify-center px-4 py-3 rounded-lg border-2 cursor-pointer transition-all ${
                formData.amenities.includes(amenity)
                  ? 'border-blue-500 bg-blue-50 text-blue-700'
                  : 'border-gray-200 bg-white hover:border-gray-300'
              }`}
            >
              <input
                type="checkbox"
                checked={formData.amenities.includes(amenity)}
                onChange={() => handleAmenityToggle(amenity)}
                className="sr-only"
              />
              <span className="text-sm font-medium capitalize">{amenity}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Custom Needs */}
      <div>
        <label htmlFor="customNeeds" className="block text-sm font-medium text-gray-700 mb-2">
          Additional Requirements (Optional)
        </label>
        <textarea
          id="customNeeds"
          value={formData.customNeeds}
          onChange={(e) => setFormData({ ...formData, customNeeds: e.target.value })}
          placeholder="E.g., Need home office, large backyard for pets, near good schools, modern kitchen..."
          rows={4}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
        />
        <p className="mt-1 text-sm text-gray-500">
          Describe any specific features or requirements you're looking for
        </p>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading}
        className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition-all ${
          loading
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700 active:scale-95'
        }`}
      >
        {loading ? 'Finding Matches...' : 'Find My Perfect Home'}
      </button>
    </form>
  );
}
