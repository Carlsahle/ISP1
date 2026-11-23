'use client';

import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="min-h-screen w-full bg-[#0B0F19] text-slate-100 flex flex-col justify-between overflow-y-auto selection:bg-slate-700 selection:text-white">
      
      <header className="w-full max-w-7xl mx-auto px-6 py-6 flex items-center justify-between border-b border-slate-800/60">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10">
            
          </div>
          <span className="text-xl font-bold tracking-wider text-slate-100">
            Grupp 19
          </span>
        </div>
        
        <div className="flex items-center gap-4">
          <Link
            href="/login"
            className="px-5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-200 text-sm font-semibold transition-all flex items-center gap-2"
          >
            Logga in
          </Link>
        </div>
      </header>

      <main className="w-full max-w-7xl mx-auto px-6 py-12 lg:py-20 space-y-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          
          <div className="space-y-6">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-[1.1]">
              Inovatum Science Park <span className="text-transparent bg-clip-text bg-gradient-to-r from-slate-200 to-slate-400"></span>
            </h1>

            <p className="text-slate-400 text-base sm:text-lg leading-relaxed">
              Detta projektet går ut på att optimera energiförbrukningen för ett industriområde, man ska kunna anpassa sin förbrukning genom att planera i förväg med två veckors samt 48 h intervall.
            </p>

            <div className="flex flex-col sm:flex-row items-center gap-4 pt-2">
             
            </div>
          </div>


        </div>
      </main>

      <footer className="w-full max-w-7xl mx-auto px-6 py-8 border-t border-slate-800/60 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
        <div>
          © 2026 
        </div>
        <div className="flex items-center gap-6"></div>
      </footer>

    </div>
  );
}