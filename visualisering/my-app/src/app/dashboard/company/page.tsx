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
        </div>
    );
}