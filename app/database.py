from pymongo import MongoClient
from pymongo.server_api import ServerApi
from .models.user_model import User
from passlib.hash import bcrypt

uri = "mongodb+srv://admin123:admin321@cluster0.olnc6fu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["streaming_anime"]
users_collection = db["users"]

def get_user(filter = str, username = str):
    user = users_collection.find_one({filter: username})
    return user

def add_user(user: User):
    user.password = bcrypt.hash(user.password)
    users_collection.insert_one(user.dict())

def update_user(username, user):
    users_collection.update_one({"username": username}, {"$set": user})

def delete_user(username):
    users_collection.delete_one({"username": username})