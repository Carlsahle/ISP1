import EffectLineChart from "../../components/charts/EffectLineChart";

export function generateStaticParams() {
  return [
    { companyId: "foretag1" },
    { companyId: "foretag2" },
    { companyId: "foretag3" },
    { companyId: "foretag4" },
  ];
}

const COMPANY_NAMES: Record<string, string> = {
  foretag1: "Företag 1",
  foretag2: "Företag 2",
  foretag3: "Företag 3",
  foretag4: "Företag 4",
};

const data = [
  { time: "08:00", effect: 4 },
  { time: "10:00", effect: 5 },
  { time: "12:00", effect: 7 },
  { time: "14:00", effect: 6 },
  { time: "16:00", effect: 8 },
  { time: "18:00", effect: 5 }
];

export default async function CompanyPage({
  params,
}: {
  params: Promise<{ companyId: string }>;
}) {
  const { companyId } = await params;
  const companyName = COMPANY_NAMES[companyId] || companyId;

  return (
    <div className="dashboard-content">
      <h1>Mitt företag – {companyName} ({companyId})</h1>
      <section className="data-cards">
        <section className="data-card">
          <h2>Effektbehov</h2>
          <p>Aktuellt effektbehov för {companyName}</p>
          <h3>Siffra</h3>
        </section>

        <section className="data-card">
          <h2>Energiförbrukning</h2>
          <p>Total förbrukning</p>
          <h3>Siffra</h3>
        </section>
      </section>

      <section className="data-cards">
        <section className="data-card">
          <EffectLineChart data={data} />
        </section>
      </section>
    </div>
  );
}
