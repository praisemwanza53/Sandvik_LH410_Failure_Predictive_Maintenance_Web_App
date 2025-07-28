# Sandvik LH410 Failure Predictor Frontend

## Setup

1. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```
2. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

## Project Structure
- `src/App.vue`: Root component
- `src/components/`: Dashboard, Graphs, AlertCard, FailureStats, LLMExplain
- `src/services/api.js`: Axios API config

## Features
- Vue 3 + TailwindCSS
- Chart.js for graphs
- Axios for API calls 