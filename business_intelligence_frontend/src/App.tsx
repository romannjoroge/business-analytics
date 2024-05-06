import Top5BarChart from "./components/Top5BarChart"
import SummaryFigure from "./components/summary-figure"
import "./App.css";
import { useState, useEffect } from "react";
import { DashboardData, getDashboardData } from "./get-dashboard-data";

function App() {
  const [dashboardData, setDashboardData] = useState<DashboardData>();

  useEffect(() => {
    async function getData() {
      let data = await getDashboardData('Alabama');
      setDashboardData(data);
    }

    getData();
  }, [])

  return (
    <main>
        <div className="outer-box">
            <div className="summary-figures-row">
               <SummaryFigure figure={dashboardData?.totalSales ?? 0} description="Total Sales"/>
               <SummaryFigure figure={dashboardData?.productsSold ?? 0} description="No. Products Sold"/>
               <SummaryFigure figure={dashboardData?.stores ?? 0} description="No. Stores"/>
               <SummaryFigure figure={dashboardData?.productCategories ?? 0} description="No. Product Categories"/>
               <SummaryFigure figure={dashboardData?.employees ?? 0} description="No. Employees"/>
            </div>
            <div className="barcharts">
                <div className="past-5-years">
                    <p>Bar Chart Sales For Past 5 Years</p>
                </div>
                <div className="top-5">
                   <Top5BarChart/> 
                   <Top5BarChart/> 
                   <Top5BarChart/> 
                   <Top5BarChart/> 
                </div>
            </div>
        </div>
    </main>
  )
}

export default App
