from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)  #create the database tables (models)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='@', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection is successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
#             {"title": "title of post 2", "content": "content of post 2", "id": 2}]
# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p      
# def find_index_post(id):
#     # index, item
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
        
## HOME ROUTE
@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}


## RETRIEVE ALL POSTS
@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

## CREATING NEW POSTS
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(my_post: Post): 
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
                   (my_post.title, my_post.content, my_post.published))
    new_post = cursor.fetchone()
    conn.commit() 
    return {"data": new_post}

## RETRIEVE LATEST POST
@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
    latest_post = cursor.fetchone()
    return {"detail": latest_post}

## RETRIEVE A SPECIFIC POST
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),)) #weird comma rule
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}


## DELETE A POST
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),)) #convert id to string, as query is string
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

## UPDATE A POST
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content= %s, published = %s WHERE id = %s RETURNING *",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return {'data': updated_post}



