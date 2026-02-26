from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATION_SUCCESS = "File Validated Success"
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"
    FILE_EXCEEDED = "File size exceeded"
    FILE_UPLOAD_SUCCESS = "File Upload Success"
    FILE_UPLOAD_FAILED = "File Upload Failed"
    PROCESSING_FAILED = "Processing Failed"
    PROCESSING_Success = "Processing Success"