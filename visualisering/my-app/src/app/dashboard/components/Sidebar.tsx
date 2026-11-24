"use client"; /*Måste finnas*/

import Link from "next/link";
import { usePathname } from "next/navigation";


export default function Sidebar(){
    const pathname = usePathname();
    const companyID = pathname.split("/")[2];
    let overviewClassName = "sidebar-link"
    let companyClassName = "sidebar-link"

    switch(pathname.split("/")[3]){
        case("overview"):
            overviewClassName = "sidebar-active";
            break;

        case("company"):
            companyClassName = "sidebar-active"
            break;
    } 

    return(
        <nav className="sidebar">
            <h1 className="sidebar-heading"> 
                Vårgårda Industriområde
            </h1>
            <div>
                
                <Link className= {overviewClassName} href={`/dashboard/${companyID}/overview`} >
                    <img src="/factory.svg"/>
                    Översikt
                </Link>

                <Link className= {companyClassName} href={`/dashboard/${companyID}/company`}>
                    <img src="/house.svg"/>
                    Mitt företag
                </Link>

            </div>
        </nav>
    )
}