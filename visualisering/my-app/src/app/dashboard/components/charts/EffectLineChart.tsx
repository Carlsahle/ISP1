"use client";

import {useState} from "react";
import{LineChart,Line,XAxis,YAxis} from "recharts";

const data48h = [
    { time: "00:00", effect: 4 },
    { time: "06:00", effect: 5 },
    { time: "12:00", effect: 7 },
    { time: "18:00", effect: 6 },
];

const data14d = [
    { time: "Mån", effect: 4 },
    { time: "Tis", effect: 5 },
    { time: "Ons", effect: 7 },
    { time: "Tor", effect: 6 },
    { time: "Fre", effect: 8 },
    { time: "Lör", effect: 5 },
    { time: "Sön", effect: 6 },
];


export default function EffectLineChart(){
    const [period, setPeriod] = useState("48h");

    let chartData=data48h

    if (period == "14d"){
        chartData=data14d
    }

    return(
        <div>
            <select onChange={(event) => setPeriod(event.target.value)}>
                <option value="48h">48 timmar</option>
                <option value="14d">14 dagar</option>
            </select>

            <LineChart data={chartData} width={500} height={300}>
                <XAxis dataKey={"time"}/>
                <YAxis/>
                <Line dataKey={"effect"}/>
            </LineChart>

        </div>    
    );
}