from fastapi import FastAPI
app = FastAPI()

from config import db
from config.db import movies_collection
from routes.student import studentRouter
db.connectToDb() 
app.include_router(studentRouter)


        


