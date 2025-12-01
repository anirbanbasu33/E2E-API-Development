from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

# Define a class => how a post looks like
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
def get_posts():
    return {"posts": ["Post 1", "Post 2", "Post 3"]}

@app.post("/createposts")
def create_posts(my_post: Post):  
    print(my_post)
    # print(my_post.dict())  
    print(my_post.model_dump()) 
    return {"data": my_post}

# What data do we expect for a new post?
# title :str, content :str, category, Bool published, 
