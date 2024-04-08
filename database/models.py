from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Address(BaseModel):
    city: str
    country: str

class AddressUpdate(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None

class Student(BaseModel):
    id:str
    name: str
    age: int
    address: Address


#In post/creation route  "id" should not be taken as input as it is created automatically by mongodb
class StudentCreate(BaseModel):
    name: str
    age: int
    address: Address

# As in patch route all datafields are not necessary
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[AddressUpdate] = None
    
   
