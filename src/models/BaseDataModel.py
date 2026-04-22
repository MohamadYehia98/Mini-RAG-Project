from helpers.config import Settings, getSettings

class BaseDataModel :
    
    def __init__(self, db_client: object):
        self.db_client = db_client
        self.app_settings = getSettings()

        


        