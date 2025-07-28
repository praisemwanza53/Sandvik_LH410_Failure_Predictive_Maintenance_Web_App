<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 p-6">
    <div class="max-w-7xl mx-auto space-y-8">
      <!-- Header Section -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-3">
          Predictive Analytics Dashboard
        </h1>
        <p class="text-slate-600 text-lg">Real-time failure prediction and risk assessment</p>
      </div>

      <!-- Failure Trends Chart -->
      <div class="group">
        <div class="bg-white/70 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20 overflow-hidden transform transition-all duration-300 hover:shadow-2xl hover:-translate-y-1">
          <div class="bg-gradient-to-r from-indigo-500 to-purple-600 p-6">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-white/20 rounded-xl">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-white">Failure Prediction Trends</h3>
            </div>
          </div>
          <div class="p-8">
            <canvas v-if="chartData" ref="chartRef" class="h-80"></canvas>
            <div v-else class="h-80 flex items-center justify-center">
              <div class="text-center">
                <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center">
                  <svg class="w-10 h-10 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                  </svg>
                </div>
                <p class="text-slate-500 font-medium">No prediction data available</p>
                <p class="text-slate-400 text-sm mt-1">Data will appear here once predictions are generated</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Component Risk Distribution -->
      <div class="group">
        <div class="bg-white/70 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20 overflow-hidden transform transition-all duration-300 hover:shadow-2xl hover:-translate-y-1">
          <div class="bg-gradient-to-r from-emerald-500 to-teal-600 p-6">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-white/20 rounded-xl">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path>
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-white">Component Risk Distribution</h3>
            </div>
          </div>
          <div class="p-8">
            <canvas v-if="componentChartData" ref="componentChartRef" class="h-80"></canvas>
            <div v-else class="h-80 flex items-center justify-center">
              <div class="text-center">
                <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center">
                  <svg class="w-10 h-10 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path>
                  </svg>
                </div>
                <p class="text-slate-500 font-medium">No component data available</p>
                <p class="text-slate-400 text-sm mt-1">Component risk analysis will be displayed here</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Risk Level Summary -->
      <div class="group">
        <div class="bg-white/70 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20 overflow-hidden transform transition-all duration-300 hover:shadow-2xl hover:-translate-y-1">
          <div class="bg-gradient-to-r from-orange-500 to-red-600 p-6">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-white/20 rounded-xl">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.728-.833-2.498 0L4.316 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-white">Risk Level Summary</h3>
            </div>
          </div>
          <div class="p-8">
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
              <div v-for="(count, level) in riskLevelCounts" :key="level" 
                   class="group/card relative overflow-hidden">
                <div class="bg-white rounded-2xl p-6 border border-slate-200 text-center transform transition-all duration-300 hover:scale-105 hover:shadow-lg relative z-10">
                  <div class="absolute inset-0 opacity-0 group-hover/card:opacity-100 transition-opacity duration-300"
                       :class="getGradientBackground(level)"></div>
                  <div class="relative z-10">
                    <div class="text-3xl font-bold mb-2 transition-colors duration-300" 
                         :class="[getRiskColor(level), 'group-hover/card:text-white']">
                      {{ count }}
                    </div>
                    <div class="text-sm font-medium capitalize transition-colors duration-300"
                         :class="['text-slate-600', 'group-hover/card:text-white/90']">
                      {{ level.replace('_', ' ') }}
                    </div>
                  </div>
                  <div class="absolute top-2 right-2 opacity-10 group-hover/card:opacity-20 transition-opacity duration-300">
                    <svg class="w-8 h-8" :class="getRiskColor(level)" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="text-center py-8">
        <p class="text-slate-500 text-sm">
          Last updated: {{ new Date().toLocaleString() }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps({ logs: Array, predictions: Array });
const chartRef = ref(null);
const componentChartRef = ref(null);
let chartInstance = null;
let componentChartInstance = null;

const getChartData = () => {
  if (!props.predictions || props.predictions.length === 0) return null;
  
  // Group predictions by date
  const counts = {};
  props.predictions.forEach(p => {
    const date = new Date(p.predicted_at || p.timestamp || Date.now());
    const d = date.toLocaleDateString();
    counts[d] = (counts[d] || 0) + 1;
  });
  
  const labels = Object.keys(counts).sort();
  const data = labels.map(label => counts[label]);
  
  return { labels, data };
};

const getComponentChartData = () => {
  if (!props.predictions || props.predictions.length === 0) return null;
  
  // Group by component and calculate average risk
  const componentRisks = {};
  props.predictions.forEach(p => {
    const component = p.component || 'unknown';
    if (!componentRisks[component]) {
      componentRisks[component] = { total: 0, count: 0 };
    }
    componentRisks[component].total += p.overall_risk?.probability || 0;
    componentRisks[component].count += 1;
  });
  
  const labels = Object.keys(componentRisks);
  const data = labels.map(component => 
    (componentRisks[component].total / componentRisks[component].count) * 100
  );
  
  return { labels, data };
};

const riskLevelCounts = computed(() => {
  if (!props.predictions || props.predictions.length === 0) return {};
  
  const counts = {};
  props.predictions.forEach(p => {
    const risk = p.overall_risk?.risk_level || 'unknown';
    counts[risk] = (counts[risk] || 0) + 1;
  });
  
  return counts;
});

const chartData = getChartData();
const componentChartData = getComponentChartData();

const getRiskColor = (level) => {
  const colors = {
    'critical': 'text-red-500',
    'high': 'text-orange-500',
    'medium': 'text-yellow-500',
    'low': 'text-blue-500',
    'very_low': 'text-emerald-500',
    'unknown': 'text-slate-500'
  };
  return colors[level] || 'text-slate-500';
};

const getGradientBackground = (level) => {
  const gradients = {
    'critical': 'bg-gradient-to-br from-red-500 to-red-600',
    'high': 'bg-gradient-to-br from-orange-500 to-orange-600',
    'medium': 'bg-gradient-to-br from-yellow-500 to-yellow-600',
    'low': 'bg-gradient-to-br from-blue-500 to-blue-600',
    'very_low': 'bg-gradient-to-br from-emerald-500 to-emerald-600',
    'unknown': 'bg-gradient-to-br from-slate-500 to-slate-600'
  };
  return gradients[level] || 'bg-gradient-to-br from-slate-500 to-slate-600';
};

const createChart = (canvasRef, data, type = 'line') => {
  if (!data || !canvasRef.value) return null;
  
  const ctx = canvasRef.value.getContext('2d');
  
  if (type === 'line') {
    return new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [{
          label: 'Predicted Failures',
          data: data.data,
          borderColor: '#6366f1',
          backgroundColor: 'rgba(99,102,241,0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#6366f1',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8,
          pointHoverBackgroundColor: '#4f46e5',
          pointHoverBorderColor: '#ffffff',
          pointHoverBorderWidth: 3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { 
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(30,41,59,0.95)',
            titleColor: '#ffffff',
            bodyColor: '#e2e8f0',
            borderColor: 'rgba(99,102,241,0.3)',
            borderWidth: 1,
            cornerRadius: 12,
            displayColors: false,
            titleFont: { size: 14, weight: 'bold' },
            bodyFont: { size: 13 },
            padding: 12
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(148,163,184,0.1)',
              drawBorder: false
            },
            ticks: {
              color: '#64748b',
              font: { size: 12 }
            }
          },
          x: {
            grid: {
              color: 'rgba(148,163,184,0.1)',
              drawBorder: false
            },
            ticks: {
              color: '#64748b',
              font: { size: 12 }
            }
          }
        },
        interaction: {
          intersect: false,
          mode: 'index'
        }
      }
    });
  } else if (type === 'doughnut') {
    return new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: data.labels,
        datasets: [{
          data: data.data,
          backgroundColor: [
            '#ef4444', // red
            '#f97316', // orange
            '#eab308', // yellow
            '#3b82f6', // blue
            '#22c55e', // green
            '#8b5cf6', // purple
            '#06b6d4', // cyan
            '#f59e0b'  // amber
          ],
          borderWidth: 3,
          borderColor: '#ffffff',
          hoverBorderWidth: 4,
          hoverBorderColor: '#ffffff'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '65%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              padding: 25,
              usePointStyle: true,
              pointStyle: 'circle',
              font: { size: 13, weight: '500' },
              color: '#475569'
            }
          },
          tooltip: {
            backgroundColor: 'rgba(30,41,59,0.95)',
            titleColor: '#ffffff',
            bodyColor: '#e2e8f0',
            borderColor: 'rgba(99,102,241,0.3)',
            borderWidth: 1,
            cornerRadius: 12,
            displayColors: true,
            titleFont: { size: 14, weight: 'bold' },
            bodyFont: { size: 13 },
            padding: 12,
            callbacks: {
              label: function(context) {
                return `${context.label}: ${context.parsed.toFixed(1)}%`;
              }
            }
          }
        }
      }
    });
  }
};

onMounted(() => {
  // Create failure trends chart
  if (chartData) {
    chartInstance = createChart(chartRef, chartData, 'line');
  }
  
  // Create component risk chart
  if (componentChartData) {
    componentChartInstance = createChart(componentChartRef, componentChartData, 'doughnut');
  }
});

watch(() => props.predictions, () => {
  // Destroy existing charts
  if (chartInstance) {
    chartInstance.destroy();
    chartInstance = null;
  }
  if (componentChartInstance) {
    componentChartInstance.destroy();
    componentChartInstance = null;
  }
  
  // Create new charts
  const newChartData = getChartData();
  const newComponentChartData = getComponentChartData();
  
  if (newChartData) {
    chartInstance = createChart(chartRef, newChartData, 'line');
  }
  if (newComponentChartData) {
    componentChartInstance = createChart(componentChartRef, newComponentChartData, 'doughnut');
  }
}, { deep: true });
</script>