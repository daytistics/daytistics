<template>
    <div class="bg-white shadow overflow-hidden sm:rounded-lg w-full p-4">
        <canvas ref="chartRef"></canvas>
    </div>
</template>

<script setup lang="ts">
import Chart from 'chart.js/auto';

const chartRef = ref(null);
const chart = ref(null);

const data = {
    labels: [
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Oct',
        'Nov',
        'Dec',
    ],
    datasets: [
        {
            label: 'Monthly Data',
            data: [65, 59, 80, 81, 56, 55, 40, 70, 75, 62, 58, 68],
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
        },
    ],
};

const options = {
    responsive: true,
    scales: {
        y: {
            beginAtZero: true,
        },
    },
    plugins: {
        legend: {
            display: false,
        },
        title: {
            display: true,
            text: 'Flat Histogram Over Months',
        },
    },
};

onMounted(() => {
    const ctx = chartRef.value.getContext('2d');
    chart.value = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: options,
    });
});
</script>
