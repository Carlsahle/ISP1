"use client";

import{LineChart,Line,XAxis,YAxis} from "recharts";

type Measurment = {
    time: string;
    effect: number;
}

type LineChartProp = {
    actualData: Measurment[];
    forecastData: Measurment[];
}

export default function EffectLineChart({actualData, forecastData}: LineChartProp){
    const chartData = [... actualData.map(item => item.time), 
                       ... forecastData.slice(1).map(item=>item.time)];

    return(
        <LineChart width={500} height={300}>
            <XAxis ticks={chartData}/>
            <YAxis/>
            <Line data={actualData} dataKey={"effect"}/>
            <Line data={forecastData} dataKey={"effect"} strokeDasharray={"5 5"}/>
        </LineChart>
    );
}