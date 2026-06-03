from fastapi import FastAPI
from routes import base, data, nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import getSettings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser

app = FastAPI()

# Hayde bas yeshte8el l FastAPI benaffez hol l eshya
# la2enno l event byeshte8el marra wahde bas sha88el l server


#@app.on_event("startup")
async def startup_span():
    Settings = getSettings()

# Hon aam ba3mal connection 3al mongo nafso
    app.mongo_connection = AsyncIOMotorClient(Settings.MONGODB_URL)

#  Hon aam ba3mal connection 3al Database (ex. Mini-rag)
    app.db_client = app.mongo_connection[Settings.MONGODB_DATABASE]

    # Hon a5adet instance mn LLMProviderFactory wl vectordb
    llm_provider_factory = LLMProviderFactory(Settings)
    vectordb_provider_factory = VectorDBProviderFactory(Settings)
    
     # Generation Client

    app.generation_client = llm_provider_factory.create(provider_name = Settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id=Settings.GENERATION_MODEL_ID)

    # Embedding Client

    app.embedding_client = llm_provider_factory.create(provider_name = Settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id = Settings.EMBEDDING_MODEL_ID,
                                              embedding_size = Settings.EMBEDDING_MODEL_SIZE)

    # Vector DB client

    app.vectordb_client = vectordb_provider_factory.create(provider = Settings.VECTORDB_BACKEND)
    app.vectordb_client.connect()

    app.template_parser = TemplateParser(
        language = Settings.PRIMARY_LANGUAGE,
        default_lang = Settings.DEFAULT_LANGUAGE
    )


# Hayde lahetta a3mal close lal database w shutdown lal event


#@app.on_event("shutdown")
async def shutdown_span():
    app.mongo_connection.close()
    app.vectordb_client.disconnect()

# Lesh ma ba3mal events lal routes?
# la2eno l database badde sha8lo marra wahde mafeyye kel marra sha8lo beser l server bate2 
# amma l route kel marra badde sha8lo kel ma yegene request

app.on_event("startup")(startup_span)
app.on_event("shutdown")(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)