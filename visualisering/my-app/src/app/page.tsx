'use client';

import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="landing-container">
      <header className="landing-header">
        <div className="landing-brand">
          <span className="landing-logo">Grupp 19</span>
        </div>
        
        <div>
          <Link href="/login" className="btn-primary">
            Logga in
          </Link>
        </div>
      </header>

      <main className="landing-main">
        <div className="landing-hero">
          <h1>Innovatum Science Park</h1>

          <p>
            Detta projektet går ut på att optimera energiförbrukningen för ett industriområde, man ska kunna anpassa sin förbrukning genom att planera i förväg med två veckors samt 48 h intervall.
          </p>
        </div>
      </main>

      <footer className="landing-footer">
        <div>© 2026</div>
      </footer>
    </div>
  );
}
