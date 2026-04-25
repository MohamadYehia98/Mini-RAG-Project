# Depends : badal ma dal ektob object settins = settings() bkl file b3ayyetla marra bl depends
# UploadFile: lahetta a3mal upload lal file
# status : hon lahetta hadded eza good request or bad request ( 200 , 404 , ..)
from fastapi import FastAPI, APIRouter, Depends ,UploadFile , status, Request

# response : 
from fastapi.responses import JSONResponse

from helpers.config import getSettings, Settings
from controllers import DataController, ProjectController, ProcessController
import os
import aiofiles
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schema import DataChunk, Files
from models.FileModel import FileModel
from models.enumerations import FileTypeEnum

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(

    prefix="/api/v1/data",
    tags = ["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(getSettings)):
    

    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id = project_id
    )

    # Validate the file properties
    Is_Valid, Result = DataController().Validate(file=file)

    if not Is_Valid:
        return JSONResponse(
            # hayde ra2m l response ly baddo yreddo l file eza error mne5eda mn l status. 
            # (200 is good, 400 not good)
            status_code = status.HTTP_400_BAD_REQUEST,

            # content howwe shu badde red 
            content = {
                "signal" : Result,
            }

        )
    

    
    Project_dir_path = ProjectController().getProjectPath(project_id = project_id)
    file_path, file_id = DataController().Generate_Unique_FilePath(original_filename = file.filename,
                                                           project_id = project_id )
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)

    except Exception as e:
        # Hayde l log lal 5ata2 eza ana ma 3refet shu l error
        logger.error(f"Error while uploading file: {e}" )

        return JSONResponse(
            # hayde ra2m l response ly baddo yreddo l file eza error mne5eda mn l status. 
            # (200 is good, 400 not good)
            status_code = status.HTTP_400_BAD_REQUEST,

            # content howwe shu badde red 
            content = {
                "signal" : ResponseSignal.FILE_UPLOAD_FAILED.value,
            }

        )

    # Store the file into database
    file_model = await FileModel.create_instance(
        db_client = request.app.db_client
    )

    file_resource = Files(

        file_project_id = project.id,
        file_type = FileTypeEnum.FILE_TYPE,
        file_name = file_id,
        file_size = os.path.getsize(file_path)
    )

    file_record = await file_model.create_file(file = file_resource)

    return JSONResponse(
        content = {
            "signal" : ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id" : str(file_record.id),
        
        }
    )


@data_router.post("/process/{project_id}")
# Hayde hon aam 5alle l text bl pdf yet2assam la chunks
async def process_endpoint(request: Request, project_id : str, process_request : ProcessRequest):

    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset







    project_model = await ProjectModel.create_instance(
        db_client = request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id = project_id
    )

    chunk_model = await ChunkModel.create_instance(

        db_client = request.app.db_client

        )
    
    if do_reset == 1:
        _ = await chunk_model.delete_chunks_by_projectID(
            project_id = project.id
        )







    process_controller = ProcessController(project_id=project_id)
    
    file_content = process_controller.get_file_content(file_id=file_id)

    file_chunks = process_controller.process_file_content(

        file_content = file_content,
        file_id = file_id,
        chunk_size = chunk_size,
        overlap_size = overlap_size,
        
    )

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(

            status_code = status.HTTP_400_BAD_REQUEST,
            content ={
                "singal": ResponseSignal.PROCESSING_FAILED.value
            }
        )

    #  return file_chunks


    file_chunks_records = [
        
        DataChunk (
        
        chunk_text = chunk.page_content,
        chunk_metadata = chunk.metadata,
        chunk_order = i+1,
        chunk_project_id = project.id

        )
    
        for i, chunk in enumerate(file_chunks)
        ]   

    chunk_model = await ChunkModel.create_instance(

        db_client = request.app.db_client

        )

    number_records = await  chunk_model.insert_many_chunks(chunks = file_chunks_records)

    return JSONResponse(

            content = {
                "signal" : ResponseSignal.PROCESSING_Success.value,
                "Inserted_Chunks" : number_records

            }

    )
    