from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user


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

        
# first app object we reference
app.include_router(post.router)
app.include_router(user.router)


## HOME ROUTE
@app.get("/")
def root():
    return {"message": "Hello, World!"}


