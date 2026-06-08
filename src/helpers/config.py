#hayda file l config ly badde o2ra menno ma3lomet l ( .env )
from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):

    #==================== APP AND Files SETTINGS ==============================

    APP_NAME: str
    APP_VERSION : str
    

    FILE_ALLOWED_TYPES : list
    FILE_MAX_SIZE : int
    FILE_DEFAULT_CHUNK_SIZE : int

#==================== MONGO DB SETTINGS ==============================

    MONGODB_URL : str
    MONGODB_DATABASE : str

#==================== LLM Config ==============================

    GENERATION_BACKEND : str
    EMBEDDING_BACKEND : str

    OPENAI_API_KEY : str = None
    OPENAI_API_URL : str = None

    GEMINI_API_KEY : str = None

    COHERE_API_KEY : str = None

    GENERATION_MODEL_ID : str = None
    EMBEDDING_MODEL_ID : str = None
    EMBEDDING_MODEL_SIZE : int = None

    default_input_max_char : int = None
    default_output_max_char : int = None
    temperature : float = None

#==================== VECTOR DB Config ==============================

    VECTORDB_BACKEND : str
    VECTOR_DB_PATH : str
    VECTOR_DB_URL : str = None
    VECTOR_DB_API_KEY : str = None

    VECTOR_DB_DISTANCE_METHOD : str = None

    PRIMARY_LANGUAGE : str = "en"
    DEFAULT_LANGUAGE : str = "ar"


    class Config:
        env_file = ".env"

def getSettings():
    return Settings()