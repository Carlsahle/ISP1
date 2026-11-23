import Sidebar from "./components/Sidebar";

export default function DashboardLayout(
{children,}:{children: React.ReactNode;}) 
{
  return (
    <div className="flex min-h-screen">
      <Sidebar />

      <main className="dashboard-content">
        {children}
      </main>
    </div>
  );
}