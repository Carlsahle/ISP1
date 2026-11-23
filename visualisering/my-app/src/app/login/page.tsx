'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import './style.css'; 

const FORETAG_EMAILS = ['a@grupp19.se', 'b@grupp19.se', 'c@grupp19.se', 'd@grupp19.se'];

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    
    const normalizedEmail = email.toLowerCase().trim();

    if (password === '123') {
      if (normalizedEmail === 'admin@grupp19.se') {
        return router.push('/dashboard');
      }
      if (FORETAG_EMAILS.includes(normalizedEmail)) {
        return router.push('/foretag');
      }
    }

    alert('Felaktig e-post eller lösenord');
  };

  return (
    <main className="mainContainer">
      <div className="card">
        <h1 className="title">Logga in</h1>

        <form onSubmit={handleLogin} className="form">
          <input 
            type="email" 
            placeholder="E-post" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="input"
          />
          
          <input 
            type="password" 
            placeholder="Lösenord" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="input"
          />

          <button type="submit" className="button">Logga in</button>
        </form>

        <p className="footerText">
          <Link href="/">Tillbaka</Link>
        </p>
      </div>
    </main>
  );
}