<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 p-4">
    <div class="max-w-full mx-auto">
      <!-- Compact Header -->
      <div class="text-center mb-6">
        <h1 class="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-1">
          Predictive Analytics Dashboard
        </h1>
        <p class="text-slate-600 text-sm">Real-time failure prediction and risk assessment</p>
      </div>

      <!-- Three Column Layout -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 h-auto md:h-[calc(100vh-140px)]">
        <!-- Column 1: Alarm Log (with input form/JSON) -->
        <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg border border-white/20 overflow-hidden flex flex-col">
          <div class="bg-gradient-to-r from-red-500 to-orange-600 p-3 flex-shrink-0">
            <div class="flex items-center space-x-2">
              <div class="p-1.5 bg-white/20 rounded-lg">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.728-.833-2.498 0L4.316 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-white">Alarm Log</h3>
            </div>
          </div>
          <div class="flex-1 p-4 overflow-hidden flex flex-col">
            <!-- Alarm Log JSON Input Only -->
            <form @submit.prevent="submitAlarmLog" class="mb-3 space-y-2">
              <label class="block text-xs font-medium text-slate-700 mb-1">Enter Alarm Log (JSON format):</label>
              <textarea v-model="alarmJson" rows="4" class="w-full rounded border px-2 py-1 text-xs font-mono" placeholder='{"message": "...", "severity": "HIGH", "component": "...", "timestamp": "..."}' required></textarea>
              <div class="flex justify-end">
                <button type="submit" class="text-xs px-3 py-1 rounded bg-indigo-600 text-white hover:bg-indigo-700">Submit</button>
              </div>
            </form>
            <!-- Alarm Log List -->
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

        <!-- Column 2: Model Prediction (show prediction results) -->
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
          <div class="flex-1 p-4 overflow-hidden flex flex-col">
            <!-- Quick Stats -->
            <div class="grid grid-cols-3 gap-2 mb-4 flex-shrink-0">
              <div v-for="(count, level) in topRiskLevels" :key="level" 
                   class="bg-white rounded-xl p-2 border border-slate-200 text-center">
                <div class="text-lg font-bold" :class="getRiskColor(level)">{{ count }}</div>
                <div class="text-xs text-slate-600 capitalize truncate">{{ level.replace('_', ' ') }}</div>
              </div>
            </div>
            <!-- Chart and Prediction Results Area -->
            <div class="bg-slate-50 rounded-xl p-3 mb-4 flex-shrink-0" style="min-height: 120px; height: 200px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
              <template v-if="predictions && predictions.length > 0">
                <canvas v-if="chartData" ref="chartRef" class="w-full h-full mb-2"></canvas>
                <div class="w-full flex flex-col gap-4">
                  <div v-for="(prediction, index) in predictions.slice(0, 10)" :key="index"
                       class="bg-white rounded-xl p-4 border border-slate-200 shadow hover:shadow-md transition mb-2 flex flex-col gap-2">
                    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-1 mb-1">
                      <div class="flex flex-wrap items-center gap-2">
                        <span class="text-base font-bold text-indigo-700 capitalize">{{ prediction.component || 'System' }}</span>
                        <span class="px-2 py-0.5 text-xs font-semibold rounded-full border"
                              :class="getRiskBadgeColor(prediction.overall_risk?.risk_level)">
                          {{ prediction.overall_risk?.risk_level || 'Unknown' }}
                        </span>
                        <span v-if="prediction.model_version" class="ml-2 text-xs text-slate-400">v{{ prediction.model_version }}</span>
                      </div>
                      <span class="text-xs text-slate-500">Predicted: {{ formatTimestamp(prediction.predicted_at || prediction.timestamp) }}</span>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                      <div class="flex flex-col gap-1">
                        <div class="text-xs text-slate-500">Overall Probability of Failure</div>
                        <div class="flex items-center gap-2 flex-wrap">
                          <span class="text-lg font-mono font-bold text-indigo-600">{{ (prediction.overall_risk?.probability * 100 || 0).toFixed(1) }}%</span>
                          <span v-if="prediction.overall_risk?.hours_to_failure !== undefined" class="text-xs text-slate-600">({{ prediction.overall_risk.hours_to_failure }}h to failure)</span>
                          <span v-if="prediction.time_to_failure !== undefined && prediction.time_to_failure !== null" class="text-xs text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full ml-1">⏳ {{ prediction.time_to_failure }} to failure</span>
                        </div>
                        <div class="w-full bg-slate-200 rounded-full h-1.5 mt-1">
                          <div class="h-1.5 rounded-full transition-all duration-300"
                               :class="getRiskBarColor(prediction.overall_risk?.risk_level)"
                               :style="{ width: `${(prediction.overall_risk?.probability * 100 || 0)}%` }"></div>
                        </div>
                      </div>
                      <div>
                        <div class="text-xs text-slate-500 mb-1">Failure Type Breakdown</div>
                        <table class="w-full text-xs border-collapse">
                          <thead>
                            <tr class="text-slate-400">
                              <th class="text-left font-medium">Type</th>
                              <th class="text-right font-medium">Probability</th>
                              <th class="text-right font-medium">Risk</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(fail, type) in prediction.predictions" :key="type">
                              <td class="pr-2 text-slate-700">{{ type }}</td>
                              <td class="text-right font-mono">{{ (fail.probability * 100).toFixed(1) }}%</td>
                              <td class="text-right capitalize">{{ fail.risk_level }}</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
                      <div>
                        <div class="text-xs text-slate-500">Severity</div>
                        <div class="font-mono text-xs text-slate-700">{{ prediction.severity || 'N/A' }}</div>
                      </div>
                      <div>
                        <div class="text-xs text-slate-500">Timestamp</div>
                        <div class="font-mono text-xs text-slate-700">{{ formatTimestamp(prediction.timestamp) }}</div>
                      </div>
                      <div>
                        <div class="text-xs text-slate-500">Predicted At</div>
                        <div class="font-mono text-xs text-slate-700">{{ formatTimestamp(prediction.predicted_at) }}</div>
                      </div>
                      <div>
                        <div class="text-xs text-slate-500">Model Version</div>
                        <div class="font-mono text-xs text-slate-700">{{ prediction.model_version || 'N/A' }}</div>
                      </div>
                    </div>
                    <div v-if="prediction.details" class="mt-2 p-2 bg-indigo-50 border border-indigo-100 rounded text-xs text-slate-700">
                      <span class="font-semibold text-indigo-700">Details:</span> {{ prediction.details }}
                    </div>
                  </div>
                </div>
              </template>
              <template v-else>
                <div class="text-center">
                  <svg class="w-8 h-8 mx-auto mb-1 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                  </svg>
                  <p class="text-slate-500 text-xs">No prediction data</p>
                  <div class="mt-2 text-xs text-slate-400">
                    <div>Submit an alarm log to see prediction results.</div>
                    <div>Prediction fields shown below:</div>
                    <ul class="list-disc list-inside text-left mx-auto max-w-xs">
                      <li>Component</li>
                      <li>Probability of Failure</li>
                      <li>Time to Failure</li>
                      <li>Failure Type</li>
                      <li>Severity</li>
                      <li>Predicted At</li>
                      <li>Details</li>
                    </ul>
                  </div>
                </div>
              </template>
            </div>
            <!-- Predictions List (show prediction results) -->
            <div class="flex-1 overflow-y-auto space-y-2 min-h-0">
              <div v-if="predictions && predictions.length > 0">
                <div v-for="(prediction, index) in predictions.slice(0, 10)" :key="index" 
                     class="bg-slate-50 rounded-lg p-3 border border-slate-200 hover:bg-slate-100 transition-colors">
                  <div class="flex items-start justify-between mb-1">
                    <span class="text-xs font-medium text-slate-600">
                      {{ formatTimestamp(prediction.predicted_at || prediction.timestamp) }}
                    </span>
                    <span class="px-2 py-0.5 text-xs font-medium rounded-full"
                          :class="getRiskBadgeColor(prediction.overall_risk?.risk_level)">
                      {{ prediction.overall_risk?.risk_level || 'Unknown' }}
                    </span>
                  </div>
                  <p class="text-sm text-slate-800 leading-tight mb-1">
                    <span class="font-semibold">{{ prediction.component || 'System' }}</span>
                    <span>- Probability of Failure: <span class="font-mono">{{ (prediction.overall_risk?.probability * 100 || 0).toFixed(1) }}%</span></span>
                  </p>
                  <p v-if="prediction.time_to_failure" class="text-xs text-slate-600 mb-1">
                    ⏳ Time to Failure: <span class="font-mono">{{ prediction.time_to_failure }}</span>
                  </p>
                  <p v-if="prediction.failure_type" class="text-xs text-slate-600 mb-1">
                    ⚠️ Failure Type: <span class="font-mono">{{ prediction.failure_type }}</span>
                  </p>
                  <p v-if="prediction.severity" class="text-xs text-slate-600 mb-1">
                    Severity: <span class="font-mono">{{ prediction.severity }}</span>
                  </p>
                  <p v-if="prediction.predicted_at" class="text-xs text-slate-600 mb-1">
                    Predicted At: <span class="font-mono">{{ formatTimestamp(prediction.predicted_at) }}</span>
                  </p>
                  <div class="w-full bg-slate-200 rounded-full h-1.5 mb-1">
                    <div class="h-1.5 rounded-full transition-all duration-300"
                         :class="getRiskBarColor(prediction.overall_risk?.risk_level)"
                         :style="{ width: `${(prediction.overall_risk?.probability * 100 || 0)}%` }"></div>
                  </div>
                  <div v-if="prediction.details" class="mt-1 text-xs text-slate-600">
                    {{ prediction.details }}
                  </div>
                </div>
              </div>
              <div v-else class="flex items-center justify-center h-full">
                <div class="text-center">
                  <div class="w-12 h-12 mx-auto mb-2 rounded-full bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center">
                    <svg class="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2m0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                    </svg>
                  </div>
                  <p class="text-slate-500 text-sm font-medium">No predictions</p>
                  <p class="text-slate-400 text-xs">Predictions will appear here</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Column 3: AI Insights (summary/statistics from backend) -->
        <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg border border-white/20 overflow-hidden flex flex-col">
          <div class="bg-gradient-to-r from-emerald-500 to-teal-600 p-3 flex-shrink-0">
            <div class="flex items-center space-x-2">
              <div class="p-1.5 bg-white/20 rounded-lg">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-white">AI Insights</h3>
            </div>
          </div>
          <div class="flex-1 p-4 overflow-hidden flex flex-col">
            <!-- Summary Cards (live from backend) -->
            <div class="grid grid-cols-2 gap-2 mb-4 flex-shrink-0">
              <div class="bg-blue-50 rounded-xl p-3 border border-blue-100">
                <div class="text-lg font-bold text-blue-600">{{ totalPredictions }}</div>
                <div class="text-xs text-blue-700">Total Predictions</div>
              </div>
              <div class="bg-red-50 rounded-xl p-3 border border-red-100">
                <div class="text-lg font-bold text-red-600">{{ highRiskCount }}</div>
                <div class="text-xs text-red-700">High Risk Items</div>
              </div>
            </div>
            <!-- AI Explanations (live from backend, fallback to static) -->
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

      <!-- Footer -->
      <div class="text-center mt-4">
        <p class="text-slate-500 text-xs">Last updated: {{ new Date().toLocaleString() }}</p>
      </div>
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

const fetchDashboardData = async () => {
  loading.value = true;
  try {
    const res = await axios.get(import.meta.env.VITE_BACKEND_URL + '/api/logs');
    logs.value = res.data.logs || [];
    predictions.value = res.data.predictions || [];
    explanations.value = res.data.explanations || [];
  } catch (err) {
    alert('Failed to load dashboard data: ' + (err?.response?.data?.detail || err.message));
  } finally {
    loading.value = false;
  }
};

const submitAlarmLog = async () => {
  let payload;
  try {
    payload = JSON.parse(alarmJson.value);
  } catch (e) {
    alert('Invalid JSON');
    return;
  }
  try {
    // Save log
    await axios.post(import.meta.env.VITE_BACKEND_URL + '/api/logs', payload);
    // Get prediction (already saved by backend)
    const predictRes = await axios.post(import.meta.env.VITE_BACKEND_URL + '/api/predict', payload);
    const prediction = predictRes.data;
    // Merge alarm log and prediction for /api/explain
    const explainPayload = { ...payload, ...prediction };
    // Get explanation/insight
    await axios.post(import.meta.env.VITE_BACKEND_URL + '/api/explain', explainPayload);
    alarmJson.value = '';
    await fetchDashboardData();
  } catch (err) {
    let msg = 'Failed to submit log or get prediction: ';
    if (err?.response?.data) {
      if (typeof err.response.data === 'string') {
        msg += err.response.data;
      } else if (err.response.data.detail) {
        msg += err.response.data.detail;
      } else if (Array.isArray(err.response.data)) {
        msg += err.response.data.map(e => e.detail || JSON.stringify(e)).join(', ');
      } else {
        msg += JSON.stringify(err.response.data);
      }
    } else {
      msg += err.message || err;
    }
    alert(msg);
  }
};

const formatTimestamp = (timestamp) => {
  if (!timestamp) return 'N/A';
  const date = new Date(timestamp);
  return date.toLocaleString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    hour: '2-digit', 
    minute: '2-digit' 
  });
};

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
      await axios.post(import.meta.env.VITE_BACKEND_URL + '/api/insights', { insights: newInsights });
    } catch (err) {
      // Optionally handle error silently
    }
  }
}, { immediate: true });

const chartData = getChartData();

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
  if (chartData) {
    chartInstance = createChart(chartRef, chartData);
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