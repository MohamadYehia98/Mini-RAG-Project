from pydantic import BaseModel
from typing import Optional

# hayde b3arref l types te3ol variables eza badde ana da55el
#  l values w lahetta ta3mal validation
class PushRequest(BaseModel):
    
    do_reset: Optional[int] = 0

class SearchRequest(BaseModel):
    text: str
    limit: Optional[int] = 10
