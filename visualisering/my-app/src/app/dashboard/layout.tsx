import { Suspense } from "react";
import Sidebar from "./components/Sidebar";

export default function DashboardLayout(
{children,}:{children: React.ReactNode;}) 
{
  return (
    <div className="flex min-h-screen">
      
      <Suspense fallback={null}>
        <Sidebar/>
      </Suspense>
      
      <main className="dashboard-content">
        {children}
      </main>
    </div>
  );
}