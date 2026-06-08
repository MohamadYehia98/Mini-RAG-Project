from qdrant_client import models, QdrantClient
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums
from typing import List
import logging
from models.db_schema import RetrievedAnswer

class QdrantDB(VectorDBInterface):
    def __init__(self, db_path: str, distance_method: str, api_key: str = None):

        self.client = None
        self.db_path = db_path
        self.api_key = api_key
        self.distance_method = None

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT

        self.logger = logging.getLogger(__name__)

    def connect(self):
        # Support either local (filesystem) Qdrant or remote Qdrant Cloud/HTTP endpoint
        try:
            if isinstance(self.db_path, str) and (self.db_path.startswith("http://") or self.db_path.startswith("https://")):
                # remote Qdrant (hosted) expects url and optional api_key
                if self.api_key:
                    self.client = QdrantClient(url=self.db_path, api_key=self.api_key)
                else:
                    self.client = QdrantClient(url=self.db_path)
            else:
                # local embedded Qdrant using filesystem path
                self.client = QdrantClient(path = self.db_path)
        except Exception as e:
            self.logger.error(f"Failed to connect to Qdrant: {e}")
            raise

    def disconnect(self):
        self.client = None

    
    def is_collection_existed(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collection(self) -> List:
        return self.client.get_collection()

    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name=collection_name)

    def delete_collection(self, collection_name: str):
        
        if self.is_collection_existed(collection_name):
            return self.client.delete_collection(collection_name=collection_name)
        

    def create_collection(self, collection_name: str,
                          embedding_size : int,
                          do_reset: bool = False):

        if do_reset:
            _ = self.delete_collection(collection_name = collection_name)

        if not self.is_collection_existed(collection_name):
            _ = self.client.create_collection(

                collection_name = collection_name,
                vectors_config = models.VectorParams(size=embedding_size, distance = self.distance_method)
            )

            return True
        
        return False
    
    def insert_one(self, collection_name: str, text: str, vector: list,
                            metadata : dict = None,
                            record_id: str = None):
        
        if not self.is_collection_existed(collection_name):
            self.logger.error(f"cannot insert new record to non-existed collection: {collection_name}")
            return False
        
        try:
            _ = self.client.upload_records(
                collection_name = collection_name,
                records = [
                    models.Record(
                        id = record_id,
                        vector = vector,
                        payload = {
                            "text" : text,
                            "metadata": metadata
                        }
                    )
                ]
            )

        except Exception as e:
            self.logger.error(f"Error while inserting record: {e}")
            return False
        
        return True

    def insert_many(self, collection_name: str, texts: list, vectors: list,
                          metadata : list = None,
                          record_ids: list = None,
                          batch_size: int = 50):
        
        if metadata is None:
            metadata = [None] * len(texts)

        if record_ids is None:
            record_ids = list(range(len(texts)))

        for batch_index, i in enumerate(range(0, len(texts), batch_size)):
            batch_end = i + batch_size

            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_ids = record_ids[i:batch_end]

            batch_records = []
            for x in range(len(batch_texts)):
                vec = batch_vectors[x]
                if not isinstance(vec, list) or len(vec) == 0:
                    self.logger.error(f"Skipping invalid vector at global index {i + x}: {type(vec)} {vec}")
                    continue

                try:
                    batch_records.append(
                        models.Record(
                            id = batch_ids[x],
                            vector = vec,
                            payload = {
                                "text" : batch_texts[x],
                                "metadata": batch_metadata[x]
                            }
                        )
                    )
                except Exception as e:
                    self.logger.error(f"Skipping invalid record payload at global index {i + x}: {e}")
                    continue

            if not batch_records:
                self.logger.warning(f"No valid records to insert for batch {batch_index} (items {i}-{batch_end}).")
                continue

            try:
                self.client.upload_records(
                    collection_name = collection_name,
                    records = batch_records,
                )
                self.logger.info(f"Inserted batch {batch_index} into Qdrant with {len(batch_records)} records.")
            except Exception as e:
                self.logger.error(f"Error while inserting batch {batch_index} (size {len(batch_records)}) to Qdrant: {e}")
                return False

        return True 
    
    """def insert_many(self, collection_name: str, texts: list, vectors: list,
                    metadata: list = None,
                    record_ids: list = None,
                    batch_size: int = 50):

        if metadata is None:
            metadata = [None] * len(texts)

        if record_ids is None:
            record_ids = list(range(len(texts)))

        for i in range(0, len(texts), batch_size):

            batch_texts = texts[i:i + batch_size]
            batch_vectors = vectors[i:i + batch_size]
            batch_metadata = metadata[i:i + batch_size]
            batch_ids = record_ids[i:i + batch_size]

            points = []

            for x in range(len(batch_texts)):

                vec = batch_vectors[x]

                # safety check (prevents multivector + float bugs)
                if not isinstance(vec, list):
                    self.logger.error(f"Invalid vector type: {type(vec)}")
                    continue

                points.append(
                    models.PointStruct(
                        id=batch_ids[x],
                        vector=vec,
                        payload={
                            "text": batch_texts[x],
                            "metadata": batch_metadata[x]
                        }
                    )
                )

            try:
                self.client.upsert(
                    collection_name=collection_name,
                    points=points
                )

            except Exception as e:
                self.logger.error(f"Batch insert failed: {e}")
                return False

        return True """

    
    def search_by_vector(self, collection_name: str, vector: list, limit: int = 5):
        results =  self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit,
    )
        if not results or len(results) ==0:
            return None
        
        return [
            RetrievedAnswer(**{
                
                "text": result.payload["text"],
                "score": result.score,
                
            })
            for result in results
        ]



