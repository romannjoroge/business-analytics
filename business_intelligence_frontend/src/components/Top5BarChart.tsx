import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);


interface Props {
    data: Record<string, any>[],
    label: string,
    label_identifier: string,
    value_identifier: string,
    legend_label: string,
    border_color: string,
    background_color: string
}

export default function Top5BarChart(props: Props) {
    const { data, label, label_identifier, value_identifier, legend_label, border_color, background_color } = props;
    const options = {
        indexAxis: 'y' as const,
        elements: {
            bar: {
                borderWidth: 2,
            },
        },
        responsive: true,
        plugins: {
            legend: {
                position: 'top' as const,
            },
            title: {
                display: true,
                text: label,
            },
        },
    };

    const labels = data.map(e => e[label_identifier]);
    const values = data.map(e => e[value_identifier]);

    const plotData = {
        labels,
        datasets: [
            {
                label: legend_label,
                data: values,
                borderColor: border_color,
                backgroundColor: background_color,
            }
        ]
    }

    return <Bar options={options} data={plotData} />;
}
