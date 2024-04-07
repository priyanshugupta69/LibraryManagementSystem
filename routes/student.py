from fastapi import APIRouter

from models.students import Student
from config.db import student_collection
from schemas.student import serialize_students
from bson import ObjectId

studentRouter = APIRouter()

@studentRouter.get('/')
async def getStudents():
    students = serialize_students(student_collection.find({}, {"name" : 1 , "age" : 1, "_id" : 0}))
    return {"data" : students}

@studentRouter.post('/', status_code=201)
async def postStudent(student : Student):
    student_dict = dict(student)
    student_dict['address'] = dict(student.address)
    savedData = student_collection.insert_one(student_dict)
    print(savedData.inserted_id)
    return {
        "id" : str(savedData.inserted_id)
    }
  
    
    



