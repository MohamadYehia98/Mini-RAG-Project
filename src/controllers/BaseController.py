# hayda l file ly badde estad3e menno m3lomet l config file lahetta yo2rahon l DataController.

from helpers.config import getSettings , Settings
import os

#This two libraries uses for creating strings
import random
import string

class BaseController:

    def __init__(self):
        
        self.app_settings = getSettings()

        # hayda l code lahetta talle3 ana wen l path tab3ole yaany basecontroller mawjod bl controller w ba3deen 
        # src

        # yaany base dir howwe src
        self.base_dir = os.path.dirname(os.path.dirname(__file__)) 
        
        self.file_dir = os.path.join(self.base_dir, "assets/files")

        self.database_dir = os.path.join(self.base_dir, "assets/database")

    # hayde bte5od l length w betraje3le 12 7arf 3ashwe2e.
    def Generate_Random_Strings(self, length: int=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def get_database_path(self, db_name: str):

        database_path = os.path.join(self.database_dir, db_name)
        
        if not os.path.exists(database_path):
            os.makedirs(database_path)

        return database_path