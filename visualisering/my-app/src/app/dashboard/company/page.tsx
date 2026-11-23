import EffectLineChart from "../components/charts/EffectLineChart";

const data = [
    { time: "08:00", effect: 4 },
    { time: "10:00", effect: 5 },
    { time: "12:00", effect: 7 },
    { time: "14:00", effect: 6 },
    { time: "16:00", effect: 8 },
    { time: "18:00", effect: 5 }
];

export default function Company(){
    return(
        <div className="dashboard-content">
            <h1>Mitt företag ... </h1>
            <section className="data-cards">

                <section className="data-card">
                    <h2>Effektbehov</h2>
                    <p>Aktuellt effektbehov</p>
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
                    <EffectLineChart data={data}/>
                </section>
            </section>



        </div>
    );
}