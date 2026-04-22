from pydantic import BaseModel
from typing import Optional

# hayde b3arref l types te3ol variables eza badde ana da55el
#  l values w lahetta ta3mal validation
class ProcessRequest(BaseModel):
    file_id : str
    chunk_size : Optional[int] = 100
    overlap_size : Optional[int] = 20
    do_reset :  Optional[int] = 0
