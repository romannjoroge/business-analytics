import "../App.css"

interface Props {
    figure: number,
    description: string,
}
export default function SummaryFigure(props: Props) {
    return(
        <div>
           <p className="summary-figures-numbers">{props.figure}</p>
           <p>{props.description}</p>
        </div>
    );
}
