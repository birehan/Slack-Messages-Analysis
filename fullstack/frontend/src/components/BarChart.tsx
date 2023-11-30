import React from "react";
import {
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS } from "chart.js/auto";
import { Chart } from 'chart.js/auto';
import { CategoryScale } from 'chart.js';

function BarChart(props:any) {
  const chartData = props.chartData;
  const options = props.options;
  ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
  );
  
  return <Bar options={options} data={chartData} />;
}

export default BarChart;
