import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Property Matchmaker | Find Your Dream Home",
  description: "Discover your perfect home in our master-planned community using AI-powered property matching. Find homes that fit your lifestyle, budget, and preferences.",
  keywords: "real estate, property matching, AI homes, master-planned community, home finder",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
          {children}
        </div>
      </body>
    </html>
  );
}
