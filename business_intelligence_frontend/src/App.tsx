import Top5BarChart from "./components/Top5BarChart"
import SummaryFigure from "./components/summary-figure"
import "./App.css";
import { useState, useEffect } from "react";
import { DashboardData, getDashboardData } from "./get-dashboard-data";
import { DashboardSummary } from "./components/dashboard-summary";

function App() {
  const [dashboardData, setDashboardData] = useState<DashboardData>();
  const [state, setState] = useState<string>("New Mexico");

  useEffect(() => {
    async function getData() {
      let data = await getDashboardData(state);
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
                  <Top5BarChart data={dashboardData?.salesForYear ?? []} label="Sales for Past 5 Months" label_identifier="month" value_identifier="sales" legend_label="Sales" background_color='rgba(77, 108, 250, 0.5)' border_color='rgb(77, 108, 250)'/> 
                  <DashboardSummary state={state}/>
                </div>
                <div className="top-5">
                   <div className="top-5-charts"><Top5BarChart data={dashboardData?.topProducts ?? []} label="Top 5 Products" label_identifier="product" value_identifier="sales" legend_label="Sales" background_color='rgba(237, 125, 58, 0.5)' border_color='rgb(237, 125, 58)'/> </div>
                   <div className="top-5-charts"><Top5BarChart data={dashboardData?.topStores ?? []} label="Top 5 Stores" label_identifier="store" value_identifier="sales" legend_label="Sales" background_color='rgba(149, 9, 82, 0.5)' border_color='rgb(149, 9, 82)'/></div> 
                   <div className="top-5-charts"><Top5BarChart data={dashboardData?.topCategories ?? []} label="Top 5 Categories" label_identifier="category" value_identifier="sales" legend_label="Sales" background_color='rgba(247, 232, 164, 0.5)' border_color='rgb(247, 232, 164)'/></div> 
                   <div className="top-5-charts"><Top5BarChart data={dashboardData?.topCities ?? []} label="Top 5 Cities" label_identifier="city" value_identifier="sales" legend_label="Sales" background_color='rgba(112, 228, 239, 0.5)' border_color='rgb(112, 228, 239)'/></div> 
                </div>
            </div>
        </div>
    </main>
  )
}

export default App
