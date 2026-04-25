from .BaseDataModel import BaseDataModel
from .db_schema import Files
from .enumerations.DataBaseEnum import DataBaseEnum
from bson import ObjectId

class FileModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client = db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_FILE_NAME.value]

    # Hyde l function eza badde 3arref l init_collection bl init bas mafene la2eno lezem await
    # wl await lezem l func. tkon async w __init__ mafena nhotta async fa mna3mal func. tenye w mne5od object.

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client) 
        await instance.init_collection()
        return instance
    

    async def init_collection(self):

        all_collections = await self.db_client.list_collection_names()

        if DataBaseEnum.COLLECTION_PROJECT_NAME not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_FILE_NAME.value]
            index = Files.get_indexes()
            for i in index:
                await self.collection.create_index(

                    i["key"],
                    name = i["name"],
                    unique = i["unique"]

                )


    async def create_file(self, file: Files):

        result = await self.collection.insert_one(file.dict(by_alias=True, exclude_unset = True))
        file.id = result.inserted_id
        
        return file
    
    async def get_all_files(self, file_project_id: str):


        return await self.collection.find({

            "file_project_id" : ObjectId(file_project_id) if isinstance(file_project_id, str) else file_project_id
            }).to_list(length=None)
