from fastapi import FastAPI,APIRouter,HTTPException
from configurations import collection
from database.schemas import all_students
from database.models import Student, StudentUpdate, StudentCreate
from bson.objectid import ObjectId
from datetime import datetime;
from fastapi import Query


app=FastAPI()
router=APIRouter()


# get all student data route 
@router.get("/students")
async def list_students(country: str = Query(None, description="Filter by country"), 
                        age: int = Query(None, description="Filter by minimum age")):
    query = {}
    
    if country:
        query["address.country"] = country
    
    if age is not None:
        query["age"] = {"$gte": age}
        
    
    data = list(collection.find(query, {"_id": 0, "name": 1, "age": 1}))
    response_data = {"data": data} 
    return response_data

#create Student Route
@router.post("/students")
async def Create_Students(new_student: StudentCreate):
    try:
        student_dict = new_student.model_dump()  
        resp = collection.insert_one(student_dict)
        return {"status_code": 200, "id": str(resp.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")
    


# update student detail route   
@router.patch("/students/{student_id}")
async def Update_student(student_id:str,updated_student:StudentUpdate):
    try:
        id=ObjectId(student_id)
        # type(id)
        existing_student=collection.find_one({"_id":id})
        print("Received payload:", updated_student.model_dump_json()) 
        if not existing_student:
            return HTTPException(status_code="404",detail=f"student does not exists")
        # address_dict = updated_student.address.dict()

        updated_student_dict = updated_student.model_dump(exclude_unset=True)
        #If only partial address field is need to be updated
        if updated_student_dict.get('address'):
            if not updated_student_dict['address'].get('city'):
                updated_student_dict['address']['city'] = existing_student['address']['city']
            if not updated_student_dict['address'].get('country'):
                updated_student_dict['address']['country'] = existing_student['address']['country']

        resp = collection.update_one({"_id": id}, {"$set": updated_student_dict})
        return {"status code":200,"message":"Student details updated successfully"}
  
    except Exception as e:
        return HTTPException(status_code="500",detail=f"some error ocurred {e}")
    

    
#get student by id route
@router.get("/students/{student_id}")
async def Fetch_student(student_id: str):
    try:
        id = ObjectId(student_id)
        student = collection.find_one({"_id": id})
        # student["id"]=str(student['_id'])
        del student['_id']
        # print(student)
        if student:
            return student
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")
    


#delete student route
@router.delete("/students/{student_id}")
async def delete_Student(student_id:str):
    try:
        id=ObjectId(student_id)
        existing_student=collection.find_one({"_id":id})
        if not existing_student:
            return HTTPException(status_code="404",detail=f"Student does not exists")
        resp=collection.delete_one({"_id":id})
        return {"status code":200,"message":"Student details deleted successfully"}
    
    except Exception as e:
        return HTTPException(status_code="500",detail=f"some error ocurred {e}")


app.include_router(router)


