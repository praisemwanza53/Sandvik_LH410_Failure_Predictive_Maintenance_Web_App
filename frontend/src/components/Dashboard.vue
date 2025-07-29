<template>
  <div class="max-w-full mx-auto p-4">
    <div class="text-center mb-6">
      <h1 class="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-1">
        Predictive Analytics Dashboard
      </h1>
      <p class="text-slate-600 text-sm">Real-time failure prediction and risk assessment</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
      <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg border border-white/20 overflow-hidden flex flex-col">
        <div class="bg-gradient-to-r from-red-500 to-orange-600 p-3 flex-shrink-0 flex items-center space-x-2">
          <div class="p-1.5 bg-white/20 rounded-lg">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.728-.833-2.498 0L4.316 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-white">Alarm Log</h3>
        </div>
        <div class="flex-1 p-4 overflow-hidden flex flex-col">
          <form @submit.prevent="submitAlarmLog" class="mb-3 space-y-2">
            <label class="block text-xs font-medium text-slate-700 mb-1">Enter Alarm Log (JSON format):</label>
            <textarea v-model="alarmJson" rows="4" class="w-full rounded border px-2 py-1 text-xs font-mono" placeholder='{"message": "...", "severity": "HIGH", "component": "...", "timestamp": "..."}' required></textarea>
            <div class="flex justify-end">
              <button type="submit" class="text-xs px-3 py-1 rounded bg-indigo-600 text-white hover:bg-indigo-700">Submit</button>
            </div>
          </form>
          <div class="flex-1 overflow-y-auto space-y-2 min-h-0">
            <div v-if="logs && logs.length > 0">
              <div v-for="(log, index) in logs.slice(0, 20)" :key="index"
                   class="bg-slate-50 rounded-lg p-3 border border-slate-200 hover:bg-slate-100 transition-colors">
                <div class="flex items-start justify-between mb-1">
                  <span class="text-xs font-medium text-slate-600">
                    {{ formatTimestamp(log.timestamp) }}
                  </span>
                  <span class="px-2 py-0.5 text-xs font-medium rounded-full"
                        :class="getSeverityColor(log.severity)">
                    {{ log.severity || 'INFO' }}
                  </span>
                </div>
                <p class="text-sm text-slate-800 leading-tight">{{ log.message || log.description || 'No message' }}</p>
                <div v-if="log.component" class="mt-1">
                  <span class="text-xs text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">{{ log.component }}</span>
                </div>
              </div>
            </div>
            <div v-else class="flex items-center justify-center h-full">
              <div class="text-center">
                <div class="w-12 h-12 mx-auto mb-2 rounded-full bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center">
                  <svg class="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                  </svg>
                </div>
                <p class="text-slate-500 text-sm font-medium">No alarm logs</p>
                <p class="text-slate-400 text-xs">Logs will appear here</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg border border-white/20 overflow-hidden flex flex-col">
        <div class="bg-gradient-to-r from-indigo-500 to-purple-600 p-3 flex-shrink-0">
          <div class="flex items-center space-x-2">
            <div class="p-1.5 bg-white/20 rounded-lg">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-white">Model Predictions</h3>
          </div>
        </div>
        <div class="flex-1 p-0 overflow-hidden flex flex-col">
          <div class="bg-white rounded-xl p-4 border border-slate-200 shadow hover:shadow-md transition flex flex-col gap-2 max-h-80 overflow-y-auto">
            <h4 class="text-base font-bold text-indigo-700 mb-2">Latest Model Predictions</h4>
            <div v-if="predictions && predictions.length > 0">
            <table class="w-full text-xs border-collapse">
              <thead>
                <tr class="text-slate-400">
                  <th class="text-left font-medium">Component</th>
                  <th class="text-right font-medium">Probability</th>
                  <th class="text-right font-medium">Risk</th>
                  <th class="text-right font-medium">Time to Failure</th>
                  <!-- <th class="text-right font-medium">Predicted At</th>
                  <th class="text-right font-medium">Details</th> -->
                </tr>
              </thead>
              <tbody>
                <tr v-for="(prediction, index) in predictions.slice(0, 10)" :key="index" class="border-b last:border-b-0">
                  <td class="pr-2 text-slate-700 font-semibold whitespace-nowrap">{{ prediction.component || 'System' }}</td>
                  <td class="text-right font-mono">{{ (prediction.overall_risk?.probability * 100 || 0).toFixed(1) }}%</td>
                  <td class="text-right capitalize">
                    <span class="px-2 py-0.5 rounded-full font-semibold" :class="getRiskBadgeColor(prediction.overall_risk?.risk_level)">
                      {{ prediction.overall_risk?.risk_level || 'Unknown' }}
                    </span>
                  </td>
                  <td class="text-right font-mono whitespace-nowrap">
                    <span v-if="prediction.overall_risk && prediction.overall_risk.hours_to_failure !== undefined">
                      {{ prediction.overall_risk.hours_to_failure.toFixed(1) }} hrs
                    </span>
                    <span v-else class="text-slate-400">--</span>
                  </td>
                  <!-- <td class="text-right font-mono whitespace-nowrap">{{ formatTimestamp(prediction.predicted_at || prediction.timestamp) }}</td>
                  <td class="text-right max-w-[10rem] truncate" :title="prediction.details">{{ prediction.details || '--' }}</td> -->
                </tr>
              </tbody>
            </table>
            </div>
            <div v-else class="text-center text-slate-400 py-8">
              No prediction data. Submit an alarm log to see prediction results.
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg border border-white/20 overflow-hidden flex flex-col">
        <div class="bg-gradient-to-r from-green-500 to-emerald-600 p-3 flex-shrink-0">
          <div class="flex items-center space-x-2">
            <div class="p-1.5 bg-white/20 rounded-lg">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-white">Feature Status</h3>
          </div>
        </div>
        <div class="flex-1 p-4 flex flex-col gap-2">
          <div class="flex items-center justify-between py-1 border-b last:border-b-0" v-for="feature in featureStatus" :key="feature.name">
            <span class="text-sm font-medium text-slate-700">{{ feature.label }}</span>
            <span class="px-2 py-0.5 text-xs font-semibold rounded-full" :class="feature.online ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'">
              {{ feature.online ? 'Connected' : 'Offline' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1">
      <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg border border-white/20 overflow-hidden flex flex-col">
        <div class="bg-gradient-to-r from-emerald-500 to-teal-600 p-3 flex-shrink-0">
          <div class="flex items-center space-x-2">
            <div class="p-1.5 bg-white/20 rounded-lg">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-white">AI Insights</h3>
          </div>
        </div>
        <div class="flex-1 p-4 overflow-hidden flex flex-col">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2 mb-4 flex-shrink-0">
            <div class="bg-blue-50 rounded-xl p-3 border border-blue-100">
              <div class="text-lg font-bold text-blue-600">{{ totalPredictions }}</div>
              <div class="text-xs text-blue-700">Total Predictions</div>
            </div>
            <div class="bg-red-50 rounded-xl p-3 border border-red-100">
              <div class="text-lg font-bold text-red-600">{{ highRiskCount }}</div>
              <div class="text-xs text-red-700">High Risk Items</div>
            </div>
          </div>
          <div class="flex-1 overflow-y-auto space-y-3 min-h-0">
            <div v-if="aiInsights.length > 0">
              <div v-for="(insight, index) in aiInsights" :key="index"
                   class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-4 border border-blue-100">
                <div class="flex items-start space-x-3">
                  <div class="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <div class="flex-1 min-w-0">
                    <h4 class="text-sm font-semibold text-slate-800 mb-1">{{ insight.title }}</h4>
                    <p class="text-xs text-slate-600 leading-relaxed">{{ insight.explanation }}</p>
                    <div v-if="insight.recommendation" class="mt-2 p-2 bg-white/50 rounded-lg">
                      <p class="text-xs text-slate-700 font-medium">💡 Recommendation:</p>
                      <p class="text-xs text-slate-600">{{ insight.recommendation }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="space-y-3">
              <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-4 border border-blue-100">
                <div class="flex items-start space-x-3">
                  <div class="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <div class="flex-1">
                    <h4 class="text-sm font-semibold text-slate-800 mb-1">System Analysis</h4>
                    <p class="text-xs text-slate-600 leading-relaxed">Monitoring system health and analyzing patterns in real-time. AI models are continuously learning from operational data to improve prediction accuracy.</p>
                  </div>
                </div>
              </div>
              <div class="bg-gradient-to-r from-emerald-50 to-teal-50 rounded-xl p-4 border border-emerald-100">
                <div class="flex items-start space-x-3">
                  <div class="flex-shrink-0 w-8 h-8 bg-emerald-100 rounded-full flex items-center justify-center">
                    <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <div class="flex-1">
                    <h4 class="text-sm font-semibold text-slate-800 mb-1">Preventive Insights</h4>
                    <p class="text-xs text-slate-600 leading-relaxed">Early detection algorithms identify potential issues before they become critical failures, enabling proactive maintenance scheduling.</p>
                  </div>
                </div>
              </div>
              <div class="bg-gradient-to-r from-orange-50 to-yellow-50 rounded-xl p-4 border border-orange-100">
                <div class="flex items-start space-x-3">
                  <div class="flex-shrink-0 w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center">
                    <svg class="w-4 h-4 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.728-.833-2.498 0L4.316 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                    </svg>
                  </div>
                  <div class="flex-1">
                    <h4 class="text-sm font-semibold text-slate-800 mb-1">Risk Assessment</h4>
                    <p class="text-xs text-slate-600 leading-relaxed">Multi-factor risk analysis considering historical patterns, environmental conditions, and component lifecycle data to prioritize maintenance actions.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="text-center mt-4">
      <p class="text-slate-500 text-xs">Last updated: {{ new Date().toLocaleString() }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue';
import Chart from 'chart.js/auto';
import axios from 'axios';

const chartRef = ref(null);
let chartInstance = null;

// Backend-driven state
const logs = ref([]);
const predictions = ref([]);
const explanations = ref([]);
const loading = ref(false);

// Alarm log JSON input only
const alarmJson = ref('');

const getSeverityColor = (severity) => {
  const colors = {
    'CRITICAL': 'bg-red-100 text-red-800',
    'HIGH': 'bg-orange-100 text-orange-800',
    'MEDIUM': 'bg-yellow-100 text-yellow-800',
    'LOW': 'bg-blue-100 text-blue-800',
    'INFO': 'bg-slate-100 text-slate-800'
  };
  return colors[severity?.toUpperCase()] || 'bg-slate-100 text-slate-800';
};

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

const getRiskBadgeColor = (level) => {
  const colors = {
    'critical': 'bg-red-100 text-red-800',
    'high': 'bg-orange-100 text-orange-800',
    'medium': 'bg-yellow-100 text-yellow-800',
    'low': 'bg-blue-100 text-blue-800',
    'very_low': 'bg-emerald-100 text-emerald-800',
    'unknown': 'bg-slate-100 text-slate-800'
  };
  return colors[level] || 'bg-slate-100 text-slate-800';
};

const getRiskBarColor = (level) => {
  const colors = {
    'critical': 'bg-red-500',
    'high': 'bg-orange-500',
    'medium': 'bg-yellow-500',
    'low': 'bg-blue-500',
    'very_low': 'bg-emerald-500',
    'unknown': 'bg-slate-500'
  };
  return colors[level] || 'bg-slate-500';
};

const formatTimestamp = (timestamp) => {
  if (!timestamp) return 'N/A';
  const date = new Date(timestamp);
  return date.toLocaleString();
};

const submitAlarmLog = async () => {
  try {
    const parsedLog = JSON.parse(alarmJson.value);
    const response = await axios.post(import.meta.env.VITE_BACKEND_URL + '/api/alarm', parsedLog);

    // Ensure logs.value is always an array
    if (!Array.isArray(logs.value)) {
      logs.value = [];
    }
    if (response.data.log) {
      logs.value.unshift(response.data.log);
    }

    // Ensure predictions.value is always an array
    if (!Array.isArray(predictions.value)) {
      predictions.value = [];
    }
    if (response.data.prediction) {
      predictions.value.unshift(response.data.prediction);
    }

    // Ensure explanations.value is always an array
    if (!Array.isArray(explanations.value)) {
      explanations.value = [];
    }
    if (response.data.explanation) {
      explanations.value.unshift(response.data.explanation);
    }

    alarmJson.value = ''; // Clear the input
  } catch (error) {
    console.error('Error submitting alarm log:', error);
    alert('Failed to submit alarm log. Please check JSON format.');
  }
};

const fetchDashboardData = async () => {
  loading.value = true;
  try {
    const [logsRes, predictionsRes, insightsRes] = await Promise.all([
      axios.get(import.meta.env.VITE_BACKEND_URL + '/api/logs'),
      axios.get(import.meta.env.VITE_BACKEND_URL + '/api/predictions'),
      axios.get(import.meta.env.VITE_BACKEND_URL + '/api/insights') // Fetch explanations
    ]);
    logs.value = logsRes.data;
    predictions.value = predictionsRes.data;
    explanations.value = insightsRes.data; // Store explanations
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
  } finally {
    loading.value = false;
  }
};

const getChartData = () => {
  if (!predictions.value || predictions.value.length === 0) return null;
  const counts = {};
  predictions.value.forEach(p => {
    const date = new Date(p.predicted_at || p.timestamp || Date.now());
    const d = date.toLocaleDateString();
    counts[d] = (counts[d] || 0) + 1;
  });
  const labels = Object.keys(counts).sort().slice(-7); // Last 7 days
  const data = labels.map(label => counts[label]);
  return { labels, data };
};

const topRiskLevels = computed(() => {
  if (!predictions.value || predictions.value.length === 0) return {};
  const counts = {};
  predictions.value.forEach(p => {
    const risk = p.overall_risk?.risk_level || 'unknown';
    counts[risk] = (counts[risk] || 0) + 1;
  });
  // Return top 3 risk levels
  const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
  return Object.fromEntries(sorted.slice(0, 3));
});

const totalPredictions = computed(() => predictions.value?.length || 0);
const highRiskCount = computed(() => {
  if (!predictions.value) return 0;
  return predictions.value.filter(p => ['critical', 'high'].includes(p.overall_risk?.risk_level)).length;
});

// AI Insights: use latest prediction and explanation from backend, and send to backend when generated
const aiInsights = computed(() => {
  const insights = [];
  if (predictions.value && predictions.value.length > 0) {
    const latestPrediction = predictions.value[0];
    if (explanations.value && explanations.value.length > 0) {
      const latestExplanation = explanations.value[0];
      insights.push({
        title: 'System Analysis',
        explanation: latestExplanation.explanation,
        recommendation: latestExplanation.recommendation
      });
      insights.push({
        title: 'Preventive Insights',
        explanation: latestExplanation.recommendation || 'Early detection algorithms identify potential issues before they become critical failures, enabling proactive maintenance scheduling.'
      });
    }
    insights.push({
      title: 'Risk Assessment',
      explanation: `Overall risk for ${latestPrediction.component || 'system'}: ${(latestPrediction.overall_risk?.probability * 100 || 0).toFixed(1)}% (${latestPrediction.overall_risk?.risk_level || 'Unknown'}). Multi-factor risk analysis considering historical patterns, environmental conditions, and component lifecycle data to prioritize maintenance actions.`
    });
  }
  return insights;
});

// Send AI insights to backend when generated
watch(aiInsights, async (newInsights) => {
  if (newInsights && newInsights.length > 0) {
    try {
      // You might want to refine what gets sent, e.g., only new insights, or periodically
      // For now, it sends the current computed insights array.
      // This might lead to sending duplicates if not managed carefully on the backend.
      // Consider adding a unique ID to insights or a timestamp to prevent re-sending the same.
      await axios.post(import.meta.env.VITE_BACKEND_URL + '/api/insights', { insights: newInsights });
    } catch (err) {
      // Optionally handle error silently
      console.error("Error sending insights to backend:", err);
    }
  }
}, { immediate: true });

// --- Feature Status Logic ---
const featureStatus = computed(() => {
  // Only show Connected if there is at least one valid prediction for the component
  const componentsOnline = {
    failure_occurred: false,
    engine_failure: false,
    brake_failure: false,
    transmission_failure: false
  };
  predictions.value.forEach(p => {
    if (p.component === 'failure_occurred') componentsOnline.failure_occurred = true;
    if (p.component === 'engine' || p.component === 'engine_failure') componentsOnline.engine_failure = true;
    if (p.component === 'brake' || p.component === 'brake_failure') componentsOnline.brake_failure = true;
    if (p.component === 'transmission' || p.component === 'transmission_failure') componentsOnline.transmission_failure = true;
  });
  // MongoDB: treat as connected ONLY if logs.value is a non-null, non-undefined array AND has at least one log
  const mongoConnected = Array.isArray(logs.value) && logs.value !== null && logs.value !== undefined && logs.value.length > 0;
  // Failure Model: only connected if there is a prediction for 'failure_occurred'
  const failureModelConnected = componentsOnline.failure_occurred;
  return [
    { name: 'db', label: 'MongoDB', online: mongoConnected },
    { name: 'failure_occurred', label: 'Failure Model', online: failureModelConnected },
    { name: 'engine_failure', label: 'Engine Model', online: componentsOnline.engine_failure },
    { name: 'brake_failure', label: 'Brake Model', online: componentsOnline.brake_failure },
    { name: 'transmission_failure', label: 'Transmission Model', online: componentsOnline.transmission_failure },
  ];
});

const chartData = computed(() => getChartData());

const createChart = (canvasRef, data) => {
  if (!data || !canvasRef.value) return null;
  const ctx = canvasRef.value.getContext('2d');
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'Predictions',
        data: data.data,
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99,102,241,0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#6366f1',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 1,
        pointRadius: 3
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
          cornerRadius: 8,
          displayColors: false,
          titleFont: { size: 11 },
          bodyFont: { size: 10 },
          padding: 8
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(148,163,184,0.2)',
            drawBorder: false
          },
          ticks: {
            color: '#64748b',
            font: { size: 10 }
          }
        },
        x: {
          grid: {
            color: 'rgba(148,163,184,0.2)',
            drawBorder: false
          },
          ticks: {
            color: '#64748b',
            font: { size: 9 }
          }
        }
      }
    }
  });
};

onMounted(async () => {
  await fetchDashboardData();
  if (chartData.value) {
    chartInstance = createChart(chartRef, chartData.value);
  }
});

watch(predictions, () => {
  if (chartInstance) {
    chartInstance.destroy();
    chartInstance = null;
  }
  const newChartData = getChartData();
  if (newChartData) {
    chartInstance = createChart(chartRef, newChartData);
  }
}, { deep: true });
</script>