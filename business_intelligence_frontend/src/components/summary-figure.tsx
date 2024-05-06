interface Props {
    figure: number,
    description: string,
}
export default function SummaryFigure(props: Props) {
    return(
        <div>
           <p>{props.figure}</p>
           <p>{props.description}</p>
        </div>
    );
}
