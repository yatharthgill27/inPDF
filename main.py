from writer import GenerateFromTemplate
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

load_dotenv()
uri = os.getenv("MONGO_URI")

cluster = MongoClient(uri, server_api=ServerApi('1'))
try:
    cluster.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = cluster["overlay"]
collection = db["Data"]


app = FastAPI()


class inputData(BaseModel):
    id:str
    pages:list[dict] 


@app.post("/generate-pdf")
def generatepdf(json_data:inputData):
    _id = json_data.id
    overlay_data = collection.find_one({"_id":ObjectId(_id)})
    path = overlay_data["path"]
    input_data = json_data.pages
    overlay_position = overlay_data["postion"]

    gen = GenerateFromTemplate(path)

    for j in range(len(input_data)):
        input_arr = list(input_data[j].values())
        overlay_arr = list(overlay_position[j].values())
        for i in range(len(input_arr)):
             gen.addText(input_arr[i],overlay_arr[i])
        gen.nextpage()    

    gen.merge()
    generated_pdf = gen.generate()
    response = StreamingResponse(generated_pdf, media_type="application/pdf")
    response.headers["Content-Disposition"] = "attachment; filename=generated.pdf"    
    return response
    

