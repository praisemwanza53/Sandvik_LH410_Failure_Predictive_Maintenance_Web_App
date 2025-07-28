<template>
  <div v-if="latestPrediction" class="mb-8">
    <div :class="alertClass" class="rounded-xl shadow-lg p-6 border-l-4 flex flex-col md:flex-row md:items-center md:space-x-8 w-full break-words">
      <div class="flex items-start justify-between w-full">
        <div class="flex items-start space-x-4 w-full">
          <div class="flex-shrink-0">
            <div :class="iconClass" class="w-12 h-12 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="riskLevel === 'critical'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                <path v-else-if="riskLevel === 'high'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                <path v-else-if="riskLevel === 'medium'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
          <div class="flex-1 flex flex-col justify-center w-full min-w-0">
            <div class="flex items-center mb-2 w-full">
              <h3 class="text-lg font-semibold mr-3 truncate">{{ riskLabel }} Risk Alert</h3>
              <span :class="statusClass" class="px-3 py-1 rounded-full text-xs font-medium ml-2">{{ riskLevel.toUpperCase() }}</span>
            </div>
            <div class="flex flex-wrap items-center gap-4 w-full">
              <div class="flex items-center space-x-2 min-w-0">
                <span class="text-sm font-medium">Probability:</span>
                <span class="text-lg font-bold">{{ isNaN(latestPrediction.probability) ? '--' : (latestPrediction.probability * 100).toFixed(1) + '%' }}</span>
              </div>
              <div class="flex items-center space-x-2 min-w-0">
                <span class="text-sm font-medium">Component:</span>
                <span class="px-3 py-1 bg-gray-100 rounded-full text-sm font-medium break-all">{{ latestPrediction.component }}</span>
              </div>
              <div v-if="latestPrediction.hours_to_failure !== undefined" class="flex items-center space-x-2 min-w-0">
                <span class="text-sm font-medium">Hours to Failure:</span>
                <span class="text-lg font-bold">{{ isNaN(latestPrediction.hours_to_failure) ? '--' : latestPrediction.hours_to_failure.toFixed(1) + 'h' }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="flex-shrink-0">
          <div :class="statusClass" class="px-3 py-1 rounded-full text-xs font-medium">
            {{ riskLevel.toUpperCase() }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({ latestPrediction: Object });

const riskLevel = computed(() => {
  const p = props.latestPrediction?.probability || 0;
  if (p >= 0.8) return 'critical';
  if (p >= 0.6) return 'high';
  if (p >= 0.4) return 'medium';
  if (p >= 0.2) return 'low';
  return 'very_low';
});

const riskLabel = computed(() => {
  const level = riskLevel.value;
  const labels = {
    'critical': 'Critical',
    'high': 'High',
    'medium': 'Medium',
    'low': 'Low',
    'very_low': 'Very Low'
  };
  return labels[level] || 'Unknown';
});

const alertClass = computed(() => {
  const level = riskLevel.value;
  const classes = {
    'critical': 'bg-red-50 border-red-500 text-red-800',
    'high': 'bg-orange-50 border-orange-500 text-orange-800',
    'medium': 'bg-yellow-50 border-yellow-500 text-yellow-800',
    'low': 'bg-blue-50 border-blue-500 text-blue-800',
    'very_low': 'bg-green-50 border-green-500 text-green-800'
  };
  return classes[level] || 'bg-gray-50 border-gray-500 text-gray-800';
});

const iconClass = computed(() => {
  const level = riskLevel.value;
  const classes = {
    'critical': 'bg-red-100 text-red-600',
    'high': 'bg-orange-100 text-orange-600',
    'medium': 'bg-yellow-100 text-yellow-600',
    'low': 'bg-blue-100 text-blue-600',
    'very_low': 'bg-green-100 text-green-600'
  };
  return classes[level] || 'bg-gray-100 text-gray-600';
});

const statusClass = computed(() => {
  const level = riskLevel.value;
  const classes = {
    'critical': 'bg-red-100 text-red-800',
    'high': 'bg-orange-100 text-orange-800',
    'medium': 'bg-yellow-100 text-yellow-800',
    'low': 'bg-blue-100 text-blue-800',
    'very_low': 'bg-green-100 text-green-800'
  };
  return classes[level] || 'bg-gray-100 text-gray-800';
});
</script> 