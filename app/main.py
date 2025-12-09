from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)  #create the database tables (models)

app = FastAPI()

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

        
## HOME ROUTE
@app.get("/")
def root():
    return {"message": "Hello, World!"}


## GET ALL POSTS
# we want a list of our specfic schema models as response = list of posts
@app.get("/posts", response_model= List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

## CREATING NEW POSTS
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(my_post: schemas.PostCreate, db: Session = Depends(get_db)): 
    new_post = models.Post(**my_post.model_dump())  #unpacks the dictionary, unpacks all fields from our model
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  #get the new post from the database
    return new_post # new_post is a sqlalchemy model instance (ORM model) --> must be converted to pydantic model (refer orm in schemas.py)

## GET LATEST POST
@app.get("/posts/latest", response_model=schemas.Post)
def get_latest_post(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    return latest_post

## GET AN INDIVIDUAL POST
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


## DELETE A POST
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

## UPDATE A POST
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()





