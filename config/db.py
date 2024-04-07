from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
load_dotenv()


uri = os.getenv('DATABASE_URL')

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
def connectToDb():
   try:
      client.admin.command('ping')
      print("Pinged your deployment. You successfully connected to MongoDB!")
   except Exception as e:
      print(e)

movies_collection = client.sample_mflix.movies
student_collection = client.library.student
if __name__ == '__main__':
    connectToDb()

