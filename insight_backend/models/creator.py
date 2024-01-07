from typing import List,Dict,Optional
from pydantic import BaseModel

class CreatorProfile(BaseModel):
    id:int
    user:Dict


