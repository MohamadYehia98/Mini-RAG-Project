#hayda file l upload file wl validation tab3olo

from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os

class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576 # Covert MB to BYTE

    def Validate(self, file: UploadFile):
        
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATION_SUCCESS.value
        



    def Generate_Unique_FilePath(self, original_filename: str, project_id: str):

        random_key = self.Generate_Random_Strings()

        project_path = ProjectController().getProjectPath(project_id = project_id)

        cleaned_filename = self.getCleanfileName(original_filename = original_filename)

        new_file_path = os.path.join(project_path, random_key + "_" + cleaned_filename)

        while os.path.exists(new_file_path):

            random_key = self.Generate_Random_Strings()
            new_file_path = os.path.join(project_path, random_key + "_" + cleaned_filename)

        return new_file_path, random_key + "_" + cleaned_filename


    def getCleanfileName(self, original_filename: str):

        # Remove any special chars except underscore
        cleaned_filename = re.sub(r'[^\w.]', '', original_filename.strip())

        # Replace spaces with underscore
        cleaned_filename = cleaned_filename.replace(" ","_")

        return cleaned_filename

