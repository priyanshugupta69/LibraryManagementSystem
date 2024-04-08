from fastapi import APIRouter, HTTPException
from fastapi import Path, Body


from models.students import Student
from config.db import student_collection
from schemas.student import serialize_students
from schemas.student import serialize_student
from bson import ObjectId

studentRouter = APIRouter()

@studentRouter.get('/')
async def getStudents():
    try:
       students = serialize_students(student_collection.find({}, {"name" : 1 , "age" : 1, "_id" : 0}))
       return {"data" : students}
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))


@studentRouter.post('/', status_code=201)
async def postStudent(student : Student):
    try:
       student_dict = dict(student)
       student_dict['address'] = dict(student.address)
       savedData = student_collection.insert_one(student_dict)
       print(savedData.inserted_id)
       return {
        "id" : str(savedData.inserted_id)
       }
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))

@studentRouter.get('/{id}', status_code=200)
async def getStudent(id: str = Path(...)):
    try:
       student = serialize_student(student_collection.find_one({"_id" : ObjectId(id) }))
       return student
    except:
       raise HTTPException(status_code=404, detail="Item not found")
    

@studentRouter.patch('/{id}', status_code= 204)
async def patchStudent(id : str = Path(...), updatedfields : dict = Body):
    try:
        print(id , updatedfields)
        result = student_collection.update_one({"_id": ObjectId(id)}, {"$set": updatedfields})
        return
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
@studentRouter.delete('/{id}', status_code= 200)
async def deleteStudent(id : str = Path(...)):
    try:
        print(id)
        result = student_collection.delete_one({"_id" : ObjectId(id)})
        print(result)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500 , detail= str(e))

  
    
    



