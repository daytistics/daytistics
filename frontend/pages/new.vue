<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
    <h1 class="text-3xl font-bold mb-8">Dashboard</h1>
    
    <div class="w-full max-w-4xl bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">Activity Chart</h2>
      <div class="flex space-x-4 mb-4">
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
    
    <div class="w-full max-w-4xl bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">Activity Recommendations</h2>
      <div class="flex flex-col space-y-4">
        <div v-for="activity in activities" :key="activity" class="flex">
          <div class="bg-blue-100 rounded-lg p-3 max-w-xs">
            <p>{{ activity }}</p>
          </div>
        </div>
        <div class="flex justify-end">
          <div class="bg-green-100 rounded-lg p-3 max-w-xs">
            <p>Which activity would you like a recommendation for?</p>
          </div>
        </div>
      </div>
    </div>
    
    <button @click="joinDiscord" class="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">
      Join Discord
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

const factor1 = ref('sleep')
const factor2 = ref('productivity')
const chartCanvas = ref(null)
let chart = null

const activities = ref(['Exercise', 'Meditation', 'Reading', 'Cooking'])

onMounted(() => {
  createChart()
})

watch([factor1, factor2], () => {
  if (chart) {
    chart.destroy()
  }
  createChart()
})

function createChart() {
  const ctx = chartCanvas.value.getContext('2d')
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
  })
}

function generateRandomData() {
  return Array.from({ length: 20 }, () => ({
    x: Math.random() * 10,
    y: Math.random() * 10
  }))
}

function joinDiscord() {
  // Implement Discord join functionality
  console.log('Joining Discord...')
}
</script>