'use client';

import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function SelectPage() {
  const router = useRouter();

  const handleSelectCompany = (companyId: string) => {
    router.push(`/dashboard/${companyId}`);
  };

  return (
    <main className="mainContainer">
      <div className="card">
        <h1 className="title">Välj</h1>

        <div className="form">
          <button
            onClick={() => router.push('/dashboard/foretag1/overview')}
            className="button buttonPrimary"
          >
            Dashboard
          </button>

          <hr className="divider" />

          <button
            onClick={() => handleSelectCompany('foretag1')}
            className="button"
          >
            Företag 1
          </button>
          <button
            onClick={() => handleSelectCompany('foretag2')}
            className="button"
          >
            Företag 2
          </button>
          <button
            onClick={() => handleSelectCompany('foretag3')}
            className="button"
          >
            Företag 3
          </button>
          <button
            onClick={() => handleSelectCompany('foretag4')}
            className="button"
          >
            Företag 4
          </button>
        </div>

        <p className="footerText">
          <Link href="/">Tillbaka</Link>
        </p>
      </div>
    </main>
  );
}
