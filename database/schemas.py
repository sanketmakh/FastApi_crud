
from typing import List


from database.models import Student

def individual_data(student: Student) -> dict:
    return {
        "id": str(student['_id']),  
        "name": student["name"],
        "age": student["age"],
        "address": student["address"]
    }

def all_students(students: List[Student]) -> List[dict]:
    return [individual_data(student) for student in students]

