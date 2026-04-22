from pydantic import BaseModel, Field , validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    # Hyde l field lahetta hadded l details ly baddon yfoto aal db
    # ... yany required field
    project_id : str = Field (...,min_length=1)

# Hyde l validator lahetta ya3mal validation lal field

    @validator('project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
    
        return value
    

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
                    ("project_id", 1)
                ],

                "name": "project_id_index_1",

                "unique": True
            }

        ]
    
    