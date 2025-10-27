'use client';

import { MatchedHome } from '@/types';
import HomeCard from './HomeCard';

interface ResultsGridProps {
  matches: MatchedHome[];
}

export default function ResultsGrid({ matches }: ResultsGridProps) {
  if (matches.length === 0) {
    return null;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {matches.map((home) => (
        <HomeCard key={home.id} home={home} />
      ))}
    </div>
  );
}
