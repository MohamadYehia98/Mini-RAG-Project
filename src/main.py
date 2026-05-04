from fastapi import FastAPI
from routes import base, data 
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import getSettings
from stores.llm.LLMProviderFactory import LLMProviderFactory

app = FastAPI()

# Hayde bas yeshte8el l FastAPI benaffez hol l eshya
# la2enno l event byeshte8el marra wahde bas sha88el l server


#@app.on_event("startup")
async def startup_db_client():
    Settings = getSettings()

# Hon aam ba3mal connection 3al mongo nafso
    app.mongo_connection = AsyncIOMotorClient(Settings.MONGODB_URL)

#  Hon aam ba3mal connection 3al Database (ex. Mini-rag)
    app.db_client = app.mongo_connection[Settings.MONGODB_DATABASE]

    # Hon a5adet instance mn LLMProviderFactory 
    llm_provider_factory = LLMProviderFactory(Settings)

    # Generation Client

    app.generation_Client = llm_provider_factory.create(provider_name = Settings.GENERATION_BACKEND)
    app.generation_Client.set_generation_model(model_id=Settings.GENERATION_MODEL_ID)

    # Embedding Client

    app.embedding_Client = llm_provider_factory.create(provider_name = Settings.EMBEDDING_BACKEND)
    app.embedding_Client.set_embedding_model(model_id = Settings.EMBEDDING_MODEL_ID,
                                              embedding_size = Settings.EMBEDDING_MODEL_SIZE)




# Hayde lahetta a3mal close lal database w shutdown lal event


#@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_connection.close()

# Lesh ma ba3mal events lal routes?
# la2eno l database badde sha8lo marra wahde mafeyye kel marra sha8lo beser l server bate2 
# amma l route kel marra badde sha8lo kel ma yegene request

#hol badal ldecorators @app.on.event()
app.router.lifespan.on_startup.append(startup_db_client)
app.router.lifespan.on_shutdown.append(shutdown_db_client)

app.include_router(base.base_router)
app.include_router(data.data_router)