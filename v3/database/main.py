from typing import Optional

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from db_api import authenticate_user, submit_case, get_train_data, submit_user_data


class NewCaseDetail(BaseModel):
    submitted_by: str
    name: str
    father_name: str
    age: int
    mobile: int
    face_encoding: list
    image: str
    case_id: str


class UserSubmission(BaseModel):
    name: str
    location: str
    image: str
    face_encoding: list
    sub_id: str
    mobile: int


app = FastAPI()


@app.get('/login')
def authenticate(username: str, password: str, role: Optional[str]=None):
    result = authenticate_user(username, password, role)
    return {"status": result}


@app.post('/new_case')
def new_case(user_info: NewCaseDetail):
    submit_case(user_info)
    return {"status": "success"}


@app.get('/get_train_data')
def get_data(submitted_by: str):
    result = get_train_data(submitted_by)
    return result


@app.post('/user_submission')
def user_submission(submission_info: SubmissionInfo):
    submit_user_data(submission_info)
    return {"status": "success"}