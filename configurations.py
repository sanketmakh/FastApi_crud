
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus




password = "Sanketlearning@123"
encoded_password = quote_plus(password)
uri = f"mongodb+srv://sanketmakhsrm:{encoded_password}@learning.hq4erj2.mongodb.net/?retryWrites=true&w=majority&appName=Learning"


client = MongoClient(uri, server_api=ServerApi('1'))


db=client.student_db
collection=db["student"]
