import type { Metadata } from "next";
import type { ReactNode } from "react";
import Link from "next/link";

import { ThreeDBackground } from "@/components/ThreeDBackground";
import "./globals.css";

export const metadata: Metadata = {
  title: "FounderGPT",
  description: "Multi-agent startup war room demo for founder idea review.",
};

type RootLayoutProps = {
  children: ReactNode;
};

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en">
      <body>
        <ThreeDBackground />
        <header className="site-header">
          <div className="header-inner">
            <Link href="/" className="logo-link">
              <h1>FounderGPT</h1>
            </Link>
            <nav className="header-nav">
              <Link href="/" className="nav-item">Overview</Link>
              <Link href="/war-room" className="nav-item">War Room</Link>
              <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="nav-item">API Docs</a>
            </nav>
          </div>
        </header>
        {children}
        <footer className="site-footer">
          <div className="footer-inner">
            <p>&copy; {new Date().getFullYear()} FounderGPT. All rights reserved.</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
