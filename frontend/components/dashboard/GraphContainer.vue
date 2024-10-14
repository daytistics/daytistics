<template>
    <div class="w-full max-w-4xl bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-xl font-semibold mb-4">Activity Chart</h2>
        <div class="flex space-x-4 mb-4 border-t border-gray-200 pt-4">
            <select v-model="factor1" class="border rounded p-2">
                <option value="sleep">Sleep</option>
                <option value="exercise">Exercise</option>
                <option value="diet">Diet</option>
            </select>
            <select v-model="factor2" class="border rounded p-2">
                <option value="productivity">Productivity</option>
                <option value="mood">Mood</option>
                <option value="energy">Energy</option>
            </select>
        </div>
        <canvas ref="chartCanvas"></canvas>
    </div>
</template>

<script lang="ts" setup>
import Chart, { type ChartItem } from 'chart.js/auto';

const factor1 = ref('sleep');
const factor2 = ref('productivity');
const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chart: Chart | null = null;

onMounted(() => {
    createChart();
});

watch([factor1, factor2], () => {
    if (chart) {
        chart.destroy();
    }
    createChart();
});

function createChart() {
    const ctx = (chartCanvas.value as HTMLCanvasElement).getContext('2d') as ChartItem;
    chart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: `${factor1.value} vs ${factor2.value}`,
                data: generateRandomData(),
                backgroundColor: 'rgba(75, 192, 192, 0.6)'
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: factor1.value
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: factor2.value
                    }
                }
            }
        }
    });
}

function generateRandomData() {
    return Array.from({ length: 20 }, () => ({
        x: Math.random() * 10,
        y: Math.random() * 10
    }));
}
</script>
