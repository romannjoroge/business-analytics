interface Props {
    state: string
}
export function DashboardSummary(props: Props) {
    return (
        <div className="dashboard-summary">
            <p>{`Summary of ${props.state}`.toUpperCase()}</p>
        </div>
    );
}