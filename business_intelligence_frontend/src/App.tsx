import Top5BarChart from "./components/Top5BarChart"
import SummaryFigure from "./components/summary-figure"
import "./App.css";

function App() {
  return (
    <main>
        <div className="outer-box">
            <div className="summary-figures-row">
               <SummaryFigure />
               <SummaryFigure />
               <SummaryFigure />
               <SummaryFigure />
               <SummaryFigure />
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
