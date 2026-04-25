from pydantic import BaseModel, Field , validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class Files(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    file_project_id: ObjectId
    file_type: str = Field(..., min_length=1)
    file_name: str = Field(..., min_length=1)
    file_size: int = Field(ge=0, default=None)
    file_config: dict = Field(default=None)
    file_pushed_at: datetime = Field(default=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True

    # Hayde method or function lahetta a3mal indexing lal chunks yaany badal ma a3mal loop aa kel l chunk 
    # ba3mal fahras fe kel l projects m3 id w bshof kel chunk lamen teb3a

    # @ hayde decorator lahetta ma e5od object aan l class bekon esmo static method
    # Hayde l logic taba3 l indexes wl implementation tab3etta BL ProjectModel.py.  
    @classmethod
    def get_indexes(cls):

        return [
            {
                "key":[
                    ("file_project_id", 1)
                ], 

                "name": "file_project_id_index_1",

                "unique": False
            },

            {
                 "key":[
                    ("file_project_id", 1),
                    ("file_name",1)
                ],

                "name": "file_project_id_name_index_1",

                "unique": True
            }

        ]