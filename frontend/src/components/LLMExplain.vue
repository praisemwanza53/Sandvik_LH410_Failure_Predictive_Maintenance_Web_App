<template>
  <div v-if="explanation" class="space-y-6 px-2 md:px-4 xl:px-8 py-2 w-full">
    <!-- Explanation Section -->
    <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200 max-h-[30vh] overflow-auto scrollbar-thin scrollbar-thumb-blue-100 scrollbar-track-blue-50">
      <div class="flex items-start space-x-4">
        <div class="flex-shrink-0">
          <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
          </div>
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-semibold text-blue-900 mb-3">AI Analysis</h3>
          <div class="prose prose-blue max-w-none text-base md:text-lg">
            <p class="text-gray-700 leading-relaxed whitespace-pre-line">{{ explanation.explanation }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Recommendation Section -->
    <div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200 max-h-[20vh] overflow-auto scrollbar-thin scrollbar-thumb-green-100 scrollbar-track-green-50">
      <div class="flex items-start space-x-4">
        <div class="flex-shrink-0">
          <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-semibold text-green-900 mb-3">Recommended Action</h3>
          <div class="bg-white rounded-lg p-4 border border-green-200">
            <p class="text-gray-800 font-medium whitespace-pre-line">{{ explanation.recommendation }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Additional Details -->
    <div v-if="explanation.confidence || explanation.factors" class="bg-gray-50 rounded-xl p-6 max-h-[15vh] overflow-auto scrollbar-thin scrollbar-thumb-gray-200 scrollbar-track-gray-50">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Additional Details</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-if="explanation.confidence" class="bg-white rounded-lg p-4 border border-gray-200">
          <h4 class="text-sm font-medium text-gray-600 mb-2">Confidence Level</h4>
          <div class="flex items-center space-x-2">
            <div class="flex-1 bg-gray-200 rounded-full h-2">
              <div 
                class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                :style="{ width: `${explanation.confidence * 100}%` }"
              ></div>
            </div>
            <span class="text-sm font-medium text-gray-900">{{ (explanation.confidence * 100).toFixed(0) }}%</span>
          </div>
        </div>
        
        <div v-if="explanation.factors" class="bg-white rounded-lg p-4 border border-gray-200">
          <h4 class="text-sm font-medium text-gray-600 mb-2">Key Factors</h4>
          <ul class="space-y-1">
            <li v-for="(factor, index) in explanation.factors" :key="index" 
                class="text-sm text-gray-700 flex items-center">
              <span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
              {{ factor }}
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Timestamp -->
    <div class="text-xs text-gray-500 text-center">
      Analysis generated at {{ formatTimestamp(explanation.generated_at) }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({ explanation: Object });

const formatTimestamp = (timestamp) => {
  if (!timestamp) return 'Unknown time';
  return new Date(timestamp).toLocaleString();
};
</script> 