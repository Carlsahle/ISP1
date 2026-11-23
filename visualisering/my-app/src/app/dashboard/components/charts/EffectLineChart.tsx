"use client";

import{LineChart,Line,XAxis,YAxis} from "recharts";

type Measurment = {
    time: string;
    effect: number;
}

type LineChartProp = {
    data: Measurment[];
}


export default function EffectLineChart({data}: LineChartProp){

    return(
        <LineChart data={data} width={500} height={300}>
            <XAxis dataKey={"time"}/>
            <YAxis/>
            <Line dataKey={"effect"}/>
        </LineChart>
    );
}