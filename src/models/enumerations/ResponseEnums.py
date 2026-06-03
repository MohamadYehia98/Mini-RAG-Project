from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATION_SUCCESS = "File Validated Success"
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"
    FILE_EXCEEDED = "File size exceeded"
    FILE_UPLOAD_SUCCESS = "File Upload Success"
    FILE_UPLOAD_FAILED = "File Upload Failed"
    PROCESSING_FAILED = "Processing Failed"
    PROCESSING_Success = "Processing Success"
    NO_FILES_ERROR = "There is No Files Found"
    NO_ID = "No File Found With This ID"
    NO_PROJECT = "Project Not Found"
    INSERT_INTO_DATABASE = "There is Error Into Insert To DataBase"
    IS_INSERTED = "The Records Is Inserted Into DB"
    COLLECTION_INFO = "Vector DB Collection Retrieved"
    RESPONSE_RETRIEVED = "Sementic Search is Succeded"
    RAG_ANSWER_SUCCESS = "Answer Success"
    RAG_ANSWER_ERROR = "Answer Error"