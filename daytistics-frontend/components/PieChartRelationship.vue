<template>
  <div>
    <Chart type="pie" :data="chartData" :options="chartOptions" />
  </div>
</template>

<script lang="ts" setup>
const fakeData = {
  labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
  datasets: [
    {
      label: 'My First Dataset',
      data: [65, 59, 80, 81, 56, 55, 40],
      fill: false,
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }
  ]
};

const chartData = ref(fakeData);

const chartOptions = ref({
  scales: {
    y: {
      beginAtZero: true
    }
  }
});

</script>

<style></style>