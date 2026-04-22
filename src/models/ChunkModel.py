from .BaseDataModel import BaseDataModel
from .db_schema import DataChunk
from .enumerations.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne


class ChunkModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client = db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]


    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client) 
        await instance.init_collection()
        return instance
    

    async def init_collection(self):

        all_collections = await self.db_client.list_collection_names()

        if DataBaseEnum.COLLECTION_CHUNK_NAME not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
            index = DataChunk.get_indexes()
            for i in index:
                await self.collection.create_index(

                    i["key"],
                    name = i["name"],
                    unique = i["unique"]

                )

    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset = True))
        chunk._id = result.inserted_id
        return chunk

    async def get_chunk(self, chunk_id: str):
        result = await self.collection.find_one({
            "_id" : ObjectId(chunk_id)

        })

        if result is None:
            return None
        
        return DataChunk(**result)

    async def insert_many_chunks(self, chunks: list, batch_size: int=100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i: i + batch_size]

            operations = [

                InsertOne(chunks.dict(by_alias=True, exclude_unset = True))
                for chunks in batch
                
            ]

            await self.collection.bulk_write(operations)

        return len(chunks)
    

    async def delete_chunks_by_projectID(self, project_id: object):
        result = await self.collection.delete_many({

                "chunk_projectID": project_id

        })

        return result.deleted_count