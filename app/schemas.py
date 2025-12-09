from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):

    pass
### Schema for response model
class Post(PostBase):
    id: int
    created_at: datetime

    ## tells pydantic to read the data even if it is not a dict, but an ORM model (like sqlalchemy model)
    class Config:
        # orm_mode = True
        from_attributes = True