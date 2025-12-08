Starting a new project

commit_1 : used thunderclient to test APIs, before pydantic

commit_2: my_post variable had referenced Post pydantic model, since we passed it into our path ops,
          fastapi will automatically validate the data received from client based on this model
          
          my_post stores the data as pydantic model. each pydantic model has .dict method
          so convert pydantic model to dict by my_post.dict()
          .dict() is depricated ==> use .model_dump()

commit_3: Before DB, all api operations concluded
commit_4: DB operations set -- 5.01.00

#### NOTES #####

source venv/bin/activate
uvicorn main:app --reload
deactivate

# New uvicorn reload- (inside app dir, checking file named main)
uvicorn app.main:app --reload