"use client";

import {useState} from "react";
import{LineChart,Line,XAxis,YAxis} from "recharts";

type Measurment = {
    time: string;
    effect: number;
}

type LineChartProp = {
    data: Measurment[];
}


export default function EffectLineChart({data}: LineChartProp){
    const [period, setPeriod] = useState("48h");

    return(
        <div>
            <select onChange={(event) => setPeriod(event.target.value)}>
                <option value="48h">48 timmar</option>
                <option value="14d">14 dagar</option>
            </select>

            <LineChart data={data} width={500} height={300}>
                <XAxis dataKey={"time"}/>
                <YAxis/>
                <Line dataKey={"effect"}/>
            </LineChart>

        </div>    
    );
}