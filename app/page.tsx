'use client';

import { useState } from 'react';
import PreferenceForm from '@/components/PreferenceForm';
import ResultsGrid from '@/components/ResultsGrid';
import { MatchedHome, FormData } from '@/types';

export default function Home() {
  const [matches, setMatches] = useState<MatchedHome[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searched, setSearched] = useState(false);

  const handleSubmit = async (formData: FormData) => {
    setLoading(true);
    setError(null);
    setSearched(true);

    try {
      // Call the Next.js API route which proxies to FastAPI
      const response = await fetch('/api/match', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          homeType: formData.homeType,
          budget: parseInt(formData.budget),
          amenities: formData.amenities,
          customNeeds: formData.customNeeds,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch matches');
      }

      const data = await response.json();
      setMatches(data.matches || []);
    } catch (err) {
      setError('Unable to find matches. Please try again.');
      console.error('Error fetching matches:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              🏡 AI Property Matchmaker
            </h1>
            <p className="text-lg text-gray-600">
              Find Your Dream Home in Our Master-Planned Community
            </p>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold mb-4">
              Welcome to Your Future Home
            </h2>
            <p className="text-xl text-blue-100">
              Our AI-powered matchmaker helps you discover properties that perfectly 
              align with your lifestyle, budget, and dreams. Experience modern living 
              in a vibrant, master-planned community designed for connection, 
              convenience, and comfort.
            </p>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Preference Form */}
        <div className="mb-12">
          <div className="bg-white rounded-lg shadow-lg p-6 md:p-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">
              Tell Us What You're Looking For
            </h3>
            <PreferenceForm onSubmit={handleSubmit} loading={loading} />
          </div>
        </div>

        {/* Results Section */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Finding your perfect matches...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {!loading && searched && matches.length === 0 && !error && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
            <p className="text-yellow-800 text-lg">
              No properties match your exact criteria. Try adjusting your preferences 
              or budget to see more options.
            </p>
          </div>
        )}

        {!loading && matches.length > 0 && (
          <div>
            <h3 className="text-2xl font-bold text-gray-900 mb-6">
              Your Top Matches
            </h3>
            <ResultsGrid matches={matches} />
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="text-gray-400">
              © 2025 AI Property Matchmaker. Built with Next.js and FastAPI.
            </p>
            <p className="text-gray-500 text-sm mt-2">
              Demonstration project for AI-driven real estate applications
            </p>
          </div>
        </div>
      </footer>
    </main>
  );
}
