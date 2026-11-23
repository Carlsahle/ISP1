"use client";

import { BarChart, Bar, XAxis, YAxis } from "recharts";

const data =[
    {time: "08.00", effect: 4},
    {time: "09.00", effect: 5},
    {time: "10.00", effect: 6},
    {time: "11.00", effect: 7}
]

export default function EffectBarChart(){
    return(
        <BarChart data={data} width={500} height={500}>
            <XAxis dataKey={"time"} label={{value: "time", fill:"white", position: "insideBottom"}} stroke="white" width={"auto"}/>
            <YAxis label={{value: "MW", fill:"white", position: "insideLeft"}} stroke="white" height={"auto"}/>
            <Bar dataKey={"effect"} fill= "#0f172a" stroke="white" radius={[10,10,0,0]}/>
        </BarChart>       
    )
} 