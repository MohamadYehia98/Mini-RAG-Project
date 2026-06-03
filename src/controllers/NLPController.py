from .BaseController import BaseController
from models.db_schema import Project, DataChunk
from stores.llm.LLMEnum import DocumentTypeEnum
from typing import List
import json
class NLPController(BaseController):

    def __init__(self, vectordb_client, generation_client, embedding_client, template_parser):

        super().__init__()
        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser

    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()

    def reset_vector_db(self, project: Project):
        Collection_name = self.create_collection_name(project_id = project.project_id)
        return self.vectordb_client.delete_collection(collection_name = Collection_name)

    def get_vectordb_collection_info(self, project: Project):
        Collection_name = self.create_collection_name(project_id = project.project_id)
        Collection_info = self.vectordb_client.get_collection_info(collection_name = Collection_name)

        return json.loads(
            json.dumps(Collection_info, default= lambda x: x.__dict__)
        )

    def index_into_vector_db(self, project: Project, chunks: List[DataChunk],
                             chunks_ids : List[int],
                             do_reset : bool = False):
        
        # step 1: Get collection Name
        Collection_name = self.create_collection_name(project_id = project.project_id)

        # step 2: Manage Items

        texts = [c.chunk_text for c in chunks]
        metadata = [c.chunk_metadata for c in chunks]
        vectors = [

            self.embedding_client.embeded_text(text = text, document_type = DocumentTypeEnum.DOCUMENT.value)
            for text in texts
        ]

        """vectors = self.embedding_client.embeded_text(text = texts, 
                                                     document_type = DocumentTypeEnum.DOCUMENT.value)"""
        
        

        # step 3: Create collection if not exist

        _ = self.vectordb_client.create_collection(collection_name = Collection_name,
                                                    embedding_size = self.embedding_client.embedding_size,
                                                    do_reset = do_reset,)

        # step 4: Insert Into DataBase

        _ = self.vectordb_client.insert_many(

            collection_name = Collection_name,
            texts = texts,
            metadata = metadata,
            vectors = vectors,
            record_ids = chunks_ids 
        )


        return True
    
    def search_vectordb_collection(self, project: Project, text: str, limit: int = 5):
        


        # get collection Name
        Collection_name = self.create_collection_name(project_id = project.project_id)


        # get text embedding vector

        vector = self.embedding_client.embeded_text(
            text = text,
            document_type = DocumentTypeEnum.QUERY.value,
        )

        if not vector or len(vector) == 0:
            return False

        # do sementic search


        results = self.vectordb_client.search_by_vector(

            collection_name = Collection_name,
            vector = vector,
            limit = limit,

        )

        return results


    def answer_rag_question(self, project: Project, query: str, limit: int= 5):

        # Step 1: Retrieved related document


        answer, full_prompt, chat_history = None,None,None
        retrieved_document = self.search_vectordb_collection(
            project = project,
            text = query,
            limit = limit
        )

        if not retrieved_document or len(retrieved_document) == 0:
            return answer, full_prompt, chat_history
        
        # Step 2 : Contruct LLM Prompt

        system_prompt = self.template_parser.get("rag", "system_prompt")


        document_prompt = [

            self.template_parser.get("rag", "document_prompt",{

                "doc_num": idx + 1,
                "chunk_text": doc.text,

            })

            for idx, doc in enumerate(retrieved_document)
        ]


        footer_prompt = self.template_parser.get("rag","footer_prompt",{
            "query":query,

        })

        chat_history = [

            self.generation_client.construct_prompt(
            
                prompt = system_prompt,
                role = self.generation_client.enums.SYSTEM.value,

            )]
        
        full_prompt = "\n\n".join([*document_prompt, footer_prompt])

        answer = self.generation_client.generate_text(

            prompt = full_prompt,
            chat_history = chat_history,
    )
        return answer, full_prompt, chat_history
    






