from typing import Optional

import uvicorn
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

from postgres import PostgresConnection
from create_tables import create


create()


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


@app.get("/login")
def authenticate(username: str, password: str, role: Optional[str] = None):
    result = False
    query = "select * from users where username='{}' and password='{}'".format(
        username, password
    )
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        if cursor.rowcount == 1:
            result = True
    return {"status": result}


@app.post("/new_case")
def new_case(user_info: NewCaseDetail):
    submitted_by = user_info.submitted_by
    name = user_info.name
    age = user_info.age
    mobile = user_info.mobile
    father_name = user_info.father_name
    face_encoding = user_info.face_encoding
    image = user_info.image
    case_id = user_info.case_id
    query = f"insert into submitted_cases(submitted_by, name, father_name, age,\
             mobile, face_encoding, status, image, case_id) values('{submitted_by}', '{name}', '{father_name}',\
             '{age}', '{mobile}', '{face_encoding}', 'NF', '{image}', '{case_id}')"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
    return {"status": "success"}


@app.get("/get_training_data")
def get_training_data(submitted_by: str, status: str = None):
    query = "select case_id, face_encoding from submitted_cases where submitted_by='{}'".format(
        submitted_by
    )
    if status:
        query = query + "and status='NF'"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


@app.get("/get_submitted_cases")
def submitted_cases(submitted_by: str):
    query = "select * from submitted_cases where submitted_by='{}'".format(submitted_by)
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


@app.post("/user_submission")
def user_submission(user_submission: UserSubmission):
    name = user_submission.name
    location = user_submission.location
    mobile = user_submission.mobile
    image = user_submission.image
    face_encoding = user_submission.face_encoding
    sub_id = user_submission.sub_id
    status = "NC"
    query = f"insert into user_submissions(id, submitted_by, face_encoding,\
              location, mobile, image, status) values('{sub_id}', '{name}', '{face_encoding}',\
              '{location}', '{mobile}', '{image}', 'NR')"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
    return {"status": "success"}


@app.get("/user_submission")
def get_usr_submission():
    query = f"select id, face_encoding from user_submissions"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


@app.get("/get_case_details")
def case_details(case_id: str):
    query = f"select name, father_name, image, mobile, age from submitted_cases where case_id={case_id}"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


@app.get("/get_user_details")
def user_details(case_id: str):
    query = (
        f"select location, submitted_at, image from user_submissions where id={case_id}"
    )
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


@app.get("/get_confirmed_cases")
def get_confirmed_cases(submitted_by: str):
    query = f"select * from submitted_cases where submitted_by='{submitted_by}' and status='F'"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


@app.get("/change_found_status")
def change_found_status(case_id: str):
    query = f"update submitted_cases set status='F' where case_id={case_id}"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
    return {"status": "success"}


if __name__ == "__main__":
    create()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
