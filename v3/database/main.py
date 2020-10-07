from typing import Optional

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from db_api import authenticate_user, submit_case


class NewCaseDetail(BaseModel):
    submitted_by: str
    name: str
    father_name: str
    age: int
    mobile: int
    face_encoding: list
    image: str


app = FastAPI()


@app.get('/login')
def authenticate(username: str, password: str, role: Optional[str]=None):
    result = authenticate_user(username, password, role)
    return {"status": result}


@app.post('/new_case')
def new_case(user_info: NewCaseDetail):
    # print(user_info)
    submit_case(user_info)
    return {"status": "hello"}
