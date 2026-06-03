from fastapi import FastAPI, APIRouter, status, Request
from fastapi.responses import JSONResponse
from helpers.config import getSettings, Settings
import os
import logging
from models import ResponseSignal
from models.ProjectModel import ProjectModel
from models.ChunkModel import  ChunkModel
from routes.schemes.nlp import PushRequest, SearchRequest
from controllers import NLPController


logger = logging.getLogger('uvicorn.error')

nlp_router = APIRouter(

    prefix="/api/v1/nlp",
    tags = ["api_v1", "nlp"],
)

@nlp_router.post("/index/push/{project_id}")
async def index_project(request: Request, project_id: str, push_request: PushRequest):
    
    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client
    )

    chunk_model = await ChunkModel.create_instance(
        db_client = request.app.db_client
    )

    project = await project_model.get_project_or_create_one(project_id = project_id)

    if not project:

        return JSONResponse(

            status_code = status.HTTP_400_BAD_REQUEST,
            content={

                    "signal": ResponseSignal.NO_PROJECT.value,
            })
    
    nlp_controller = NLPController(
        vectordb_client = request.app.vectordb_client,
        generation_client = request.app.generation_client,
        embedding_client = request.app.embedding_client,
        template_parser = request.app.template_parser,
    )

    has_records = True
    page_no = 1
    Inserted_Items_count = 0
    idx = 0

    while has_records:
        page_chunks = await chunk_model.get_project_chunks(project_id = project.id, page_no = page_no)
        if len(page_chunks):
            page_no += 1

        if not page_chunks or len(page_chunks) == 0:
            has_records = False
            break

        chunks_ids = list(range(idx, idx + len(page_chunks)))
        idx += len(page_chunks)

        is_inserted = nlp_controller.index_into_vector_db(

            project = project,
            chunks = page_chunks,
            do_reset = push_request.do_reset,
            chunks_ids = chunks_ids,

        )

        if not is_inserted:

            return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content={

                    "signal": ResponseSignal.INSERT_INTO_DATABASE.value,
            })
        
        Inserted_Items_count += len(page_chunks)

    return JSONResponse(
            content={

                "signal": ResponseSignal.IS_INSERTED.value,
                "Inserted Item Count": Inserted_Items_count,
            })


@nlp_router.get("/index/info/{project_id}")
async def get_project_info(request: Request, project_id: str):

    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client
    )

    project = await project_model.get_project_or_create_one(project_id = project_id)


    nlp_controller = NLPController(
        vectordb_client = request.app.vectordb_client,
        generation_client = request.app.generation_client,
        embedding_client = request.app.embedding_client,
        template_parser = request.app.template_parser,
    )

    collection_info = nlp_controller.get_vectordb_collection_info(
        project = project
    )

    return JSONResponse(
            content={

                "signal": ResponseSignal.COLLECTION_INFO.value,
                "Collection_Info" : collection_info,
                
            })


@nlp_router.post("/index/search/{project_id}")
async def search_index(request: Request, project_id: str, search_request: SearchRequest):
    
    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client
    )

    project = await project_model.get_project_or_create_one(project_id = project_id)


    nlp_controller = NLPController(
        vectordb_client = request.app.vectordb_client,
        generation_client = request.app.generation_client,
        embedding_client = request.app.embedding_client,
        templae_parser = request.app.template_parser
    )

    results = nlp_controller.search_vectordb_collection(
        project = project,
        text = search_request.text,
        limit = search_request.limit,
    )

    return JSONResponse(
            content={

                "signal": ResponseSignal.RESPONSE_RETRIEVED.value,
                "Result" : [result.dict() for result in results ]
                
            })

@nlp_router.post("/rag/answer/{project_id}")
async def search_index(request: Request, project_id: str, search_request: SearchRequest):
    
    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client
    )

    project = await project_model.get_project_or_create_one(project_id = project_id)


    nlp_controller = NLPController(
        vectordb_client = request.app.vectordb_client,
        generation_client = request.app.generation_client,
        embedding_client = request.app.embedding_client,
        template_parser = request.app.template_parser
    )

    answer, full_prompt, chat_history = nlp_controller.answer_rag_question(

        project = project,
        query = search_request.text,
        limit = search_request.limit,

    )

    if not answer:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.RAG_ANSWER_ERROR.value
                }
        )
    
    return JSONResponse(
        content={
            "signal": ResponseSignal.RAG_ANSWER_SUCCESS.value,
            "answer": answer,
            "full_prompt": full_prompt,
            "chat_history": chat_history
        }
    )



