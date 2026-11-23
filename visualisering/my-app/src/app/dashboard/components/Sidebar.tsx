"use client"; /*Måste finnas*/

import Link from "next/link";
import { usePathname } from "next/navigation";


export default function Sidebar(){
    const pathname = usePathname();
    let overviewClassName = "sidebar-link"
    let companyClassName = "sidebar-link"

    switch(pathname){
        case("/dashboard/overview"):
            overviewClassName = "sidebar-active";
            break;

        case("/dashboard/company"):
            companyClassName = "sidebar-active"
            break;
    } 

    return(
        <nav className="sidebar">
            <h1 className="sidebar-heading"> 
                Vårgårda Industriområde
            </h1>
            <div>
                
                <Link className= {overviewClassName} href="/dashboard/overview">
                    <img src="/factory.svg"/>
                    Översikt
                </Link>

                <Link className= {companyClassName} href="/dashboard/company">
                    <img src="/house.svg"/>
                    Mitt företag
                </Link>

            </div>
        </nav>
    )
}