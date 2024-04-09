from fastapi import APIRouter, HTTPException
from fastapi import Path, Body, Query


from models.students import Student
from config.db import student_collection
from schemas.student import serialize_students
from schemas.student import serialize_student
from bson import ObjectId

studentRouter = APIRouter()

@studentRouter.get('/', status_code=200, summary= "List students" , description= "An API to find a list of students. You can apply filters on this API by passing the query parameters as listed below")
async def getStudents(country: str = Query(None), min_age: int = Query(None)):
    try:
       query = {}
       
       if country:
            query['address.country'] =  {"$regex": f"^{country}$", "$options": "i"}

       if min_age is not None:
            query['age'] = {"$gte": min_age}

       students = serialize_students(student_collection.find(query, {"name" : 1 , "age" : 1, "_id" : 0}))
       return {"data" : students}
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))


@studentRouter.post('/', status_code=201 ,summary="Create Students" , description="API to create a student in the system. All fields are mandatory and required while creating the student in the system.")
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

@studentRouter.get('/{id}', status_code=200, summary="Fetch student" , description="The ID of the student previously created." )
async def getStudent(id: str = Path(...)):
    try:
       student = serialize_student(student_collection.find_one({"_id" : ObjectId(id) } , {"_id" : 0}))
       return student
    except:
       raise HTTPException(status_code=404, detail="Item not found")
    

@studentRouter.patch('/{id}', status_code= 204, summary="Update student" , description="API to update the student's properties based on information provided. Not mandatory that all information would be sent in PATCH, only what fields are sent should be updated in the Database.")
async def patchStudent(id : str = Path(...), updatedfields : dict = Body):
    try:
        print(id , updatedfields)
        result = student_collection.update_one({"_id": ObjectId(id)}, {"$set": updatedfields})
        return
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    

@studentRouter.delete('/{id}', status_code= 200 , summary = "Delete student")
async def deleteStudent(id : str = Path(...)):
    try:
        print(id)
        result = student_collection.delete_one({"_id" : ObjectId(id)})
        print(result)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500 , detail= str(e))

  
    
    



