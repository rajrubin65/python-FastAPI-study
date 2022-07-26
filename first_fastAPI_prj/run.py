from importlib import reload
import uvicorn
from typing import Union
from typing import Optional
from fastapi import FastAPI,Path,File, UploadFile
from pyrsistent import optional
from pydantic import BaseModel


app = FastAPI()

employee = {
    1:{
        'name':'rubin raj',
        'age':23
    }
}

class Employee(BaseModel):
    name: str
    age: int


@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    print(q)
    return {"item_id": item_id, "q": q}



@app.get("/name")
def name():
    return "Rubin Raj"



@app.get("/get-by-id/{id}")
def get_employee(id: int = Path(None,description="Enter the ID of the Employee",gt=0)): #path param and the FastAPI path method(gt,ge,lt,le)
    return employee[id]



@app.get("/get-by-name")
def get_employee(*, name: Optional[str] = None, test:int):
    for empid in employee:
        if employee[empid]["name"] == name:  
            return employee[empid]
    return {'Data':'Not Found'}


@app.post("/create-employee/{id}")
def add_employee(id : int, emp : Employee):
    if id in employee:
        return{"msg":"Existing"}
    employee[id] = emp
    return employee[id]

@app.put("/edit-employee/{id}")
def edit_employee(id:int):
    pass

@app.post("/files/")
async def create_file(file: bytes = File()):

    # return {"file_size": len(file)}
    return file


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


if __name__ == "__main__":
    uvicorn.run(app=app,host='127.0.0.1',port = 2255)