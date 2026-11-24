type DropDownProps = {
    period: string;
    setPeriod: (period: string) => void;
}

export default function DropDown({/*props: DropDownProps */}){
    return(
        <div>
            <select className="period-dropdown">
                <option value="48h">48 timmar</option>
                <option value="14d">14 dagar</option>
            </select>
        </div>
    );
}