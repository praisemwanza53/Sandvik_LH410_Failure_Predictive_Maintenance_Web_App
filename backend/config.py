import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB Configuration
    MONGODB_URI = os.getenv(
        "MONGODB_URI", 
        "mongodb+srv://mwanzapraise700:BClMv7vNv8kuIMfa@predictive.niwoquq.mongodb.net/?retryWrites=true&w=majority&appName=predictive"
    )
    MONGODB_DB = os.getenv("MONGODB_DB", "sandvik_lh410")
    
    # Frontend Configuration
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    
    # API Configuration
    API_KEY = os.getenv("API_KEY", "test_key_123")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # OpenAI Configuration (for LLM explanations)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))

# Global config instance
config = Config() 