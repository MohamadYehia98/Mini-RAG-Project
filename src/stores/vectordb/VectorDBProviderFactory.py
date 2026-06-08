from .providers import QdrantDB
from .VectorDBEnums import VectorDBEnums
from controllers.BaseController import BaseController

class VectorDBProviderFactory:

    def __init__(self, config):

        self.config = config
        self.base_controller = BaseController()

    def create(self, provider: str):

        if provider == VectorDBEnums.QDRANT.value:
            # If a remote Qdrant URL is provided in config, use it; otherwise use local path
            if hasattr(self.config, 'VECTOR_DB_URL') and self.config.VECTOR_DB_URL:
                db_path = self.config.VECTOR_DB_URL
                api_key = getattr(self.config, 'VECTOR_DB_API_KEY', None)
            else:
                db_path = self.base_controller.get_database_path(db_name = self.config.VECTOR_DB_PATH)
                api_key = None

            return QdrantDB(
                db_path = db_path,
                distance_method = self.config.VECTOR_DB_DISTANCE_METHOD,
                api_key = api_key,
            )


