# Sandvik LH410 Failure Predictive Maintenance Web App

A modern, AI-powered predictive maintenance system for Sandvik LH410 mining equipment. This application uses machine learning models to predict equipment failures and provides real-time monitoring with a beautiful, responsive web interface.

## 🚀 Features

- **AI-Powered Predictions**: Uses trained machine learning models to predict equipment failures
- **Real-time Monitoring**: Live dashboard with failure statistics and trends
- **Beautiful UI**: Modern, responsive design with Tailwind CSS
- **Component Analysis**: Detailed analysis for engine, brake, transmission, and electrical systems
- **Risk Assessment**: Multi-level risk classification (critical, high, medium, low, very low)
- **AI Explanations**: LLM-powered explanations for predictions and recommendations (using Groq LLM)
- **Interactive Charts**: Real-time data visualization with Chart.js
- **RESTful API**: FastAPI backend with comprehensive endpoints

## Project Status

Currently in **Beta** development. The core functionality is implemented and undergoing testing.

## Future Enhancements

- Implement user authentication and authorization.
- Add more detailed failure analysis and reporting.
- Integrate with additional data sources.
- Improve model accuracy through ongoing training and optimization.

## Data Sources

The system uses alarm logs and sensor data from Sandvik LH410 mining equipment. The data is stored in CSV files and used for training the machine learning models.

## Model Training

The machine learning models are trained using a combination of historical alarm data and sensor readings. The training process involves data preprocessing, feature engineering, model selection (e.g., XGBoost), and hyperparameter tuning. Training scripts are located in the `data/` directory.

## 🏗️ Architecture

```
├── backend/                 # FastAPI backend
│   ├── core/               # Core ML models and Groq LLM integration
│   ├── db/                 # Database models and MongoDB integration
│   ├── routes/             # API endpoints
│   └── utils/              # Utility functions
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── components/     # Vue components
│   │   └── services/       # API services
└── data/                   # ML models and training data
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **Scikit-learn**: Machine learning models
- **XGBoost**: Gradient boosting for predictions
- **MongoDB**: Database for logs and predictions
- **Groq**: LLM integration for explanations

### Frontend
- **Vue.js 3**: Progressive JavaScript framework
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js**: Interactive charts and graphs
- **Vite**: Fast build tool and dev server

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB (optional, for data persistence)

### Backend Setup

1. **Activate virtual environment**:
   ```bash
   .\activate_env.bat
   ```

2. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Start the backend server**:
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**:
   ```bash
   cd frontend
   npm run dev
   ```

## 🚀 Quick Start

1. **Start both servers**:
   ```bash
   # Terminal 1 - Backend
   .\activate_env.bat
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

2. **Access the application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📊 API Endpoints

### Core Endpoints
- `GET /api/health` - Health check
- `POST /api/predict` - Predict equipment failure
- `GET /api/logs` - Get historical logs and predictions
- `POST /api/explain` - Get AI explanation for prediction

### Example Prediction Request
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "alarm_type": "temperature_high",
  "component": "engine",
  "severity": "high",
  "location": "front",
  "count": 3,
  "spn": 123,
  "fmi": 4,
  "hours": 1500.5
}
```

## 🎯 Machine Learning Models

The system includes trained models for:
- **Overall Failure Prediction**: General equipment failure probability
- **Engine Failure**: Specific engine component failure prediction
- **Brake Failure**: Brake system failure prediction
- **Transmission Failure**: Transmission system failure prediction

Each model provides:
- Failure probability (0-1)
- Risk level classification
- Hours to failure estimation

## 🎨 UI Components

### Dashboard Features
- **Statistics Cards**: Real-time failure counts, active alarms, and monitored components
- **Risk Alerts**: Color-coded alerts based on failure probability
- **Interactive Charts**: 
  - Failure prediction trends over time
  - Component risk distribution
  - Risk level summary
- **AI Explanations**: Detailed analysis and recommendations
- **System Status**: Backend health and model status

### Design Highlights
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Clean, professional interface with gradients and shadows
- **Real-time Updates**: Live data refresh and status indicators
- **Accessibility**: Proper contrast ratios and keyboard navigation

## 🔧 Configuration

### Environment Variables
The application is pre-configured with MongoDB Atlas connection. To customize settings, create a `.env` file in the backend directory:

```env
# MongoDB Configuration (pre-configured)
MONGODB_URI=mongodb+srv://mwanzapraise700:BClMv7vNv8kuIMfa@predictive.niwoquq.mongodb.net/?retryWrites=true&w=majority&appName=predictive
MONGODB_DB=sandvik_lh410

# Frontend Configuration
FRONTEND_ORIGIN=http://localhost:5173

# API Configuration
API_KEY=test_key_123
```

### Model Configuration
- Models are automatically loaded from the `data/` directory
- Supports hot-reloading for model updates
- Fallback handling for missing models

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -c "from core.model import predictor; print('Models loaded:', list(predictor.models.keys()))"
```

### Frontend Testing
```bash
cd frontend
npm run build
```

## 📈 Performance

- **Backend**: FastAPI with async/await for high concurrency
- **Frontend**: Vue.js 3 with Composition API for optimal performance
- **Models**: Optimized scikit-learn models with joblib serialization
- **Charts**: Efficient Chart.js rendering with data virtualization

## 🔒 Security

- **CORS Configuration**: Properly configured for production
- **Rate Limiting**: API rate limiting with slowapi
- **Input Validation**: Pydantic models for data validation
- **Authentication**: API key authentication (configurable)

## 🚀 Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### Manual Deployment
1. Build frontend: `cd frontend && npm run build`
2. Start backend: `cd backend && uvicorn main:app --host 0.0.0.0 --port 8000`
3. Serve frontend build files with a web server

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the API documentation at http://localhost:8000/docs
- Review the backend logs for error details
- Ensure all dependencies are properly installed.

## 🚀 Deployment Considerations

- Ensure sufficient resources (CPU, memory) for the backend and frontend.
- Configure appropriate environment variables for production.
- Monitor application logs for errors and performance bottlenecks.
- Implement health checks for monitoring and alerting.

## Troubleshooting

- **Backend not starting:** Check the backend logs for errors. Verify that the virtual environment is activated and dependencies are installed.
- **Frontend not displaying:** Ensure the frontend is built and the web server is serving the correct files. Check the browser's developer console for errors.
- **API errors:** Verify the API endpoints and request parameters. Check the backend logs for error details.

## 🎉 Success!

Your Sandvik LH410 Failure Predictive Maintenance Web App is now ready! The system provides:

✅ **Working ML Models**: All 4 prediction models loaded and functional  
✅ **Beautiful Frontend**: Modern, responsive UI with real-time updates  
✅ **Robust Backend**: FastAPI server with comprehensive API endpoints  
✅ **MongoDB Integration**: Cloud database with automatic data persistence  
✅ **Real-time Monitoring**: Live dashboard with interactive charts  
✅ **AI Explanations**: LLM-powered insights and recommendations  

The application is now ready for local testing and can be deployed to production environments.
