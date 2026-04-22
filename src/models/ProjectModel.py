from .BaseDataModel import BaseDataModel
from .db_schema import Project
from .enumerations.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client = db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

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
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            index = Project.get_indexes()
            for i in index:
                await self.collection.create_index(

                    i["key"],
                    name = i["name"],
                    unique = i["unique"]

                )




    async def create_project(self, project: Project):
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset = True))
        project._id = result.inserted_id
        return project
    
    async def get_project_or_create_one(self, project_id: str):
        record = await self.collection.find_one({
            "project_id" : project_id
        })

        if record is None:
            #create new one
            project = Project(project_id = project_id)
            project = await self.create_project(project = project)

            return project

        # (**) hayde lahetta yhawwel l record dictionary la Project Model
        return Project(**record)


    async def get_all_projects(self, page :int=1, page_size: int=10):
        
        #count total numbers of documents
        total_documents = await self.collection.count_documents({})

        #calculate total number of documents

        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages += 1

        cursor = self.collection.find().skip({page-1} * page_size).limit(page_size)
        projects=[]

        async for document in cursor:
            projects.append(
                Project(**document)
            )

        return projects, total_pages


