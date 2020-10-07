import psycopg2

from postgres import PostgresConnection


def authenticate_user(username, password, role):
    query = "select * from users where username='{}' and password='{}'".format(username, password)
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        if cursor.rowcount == 1:
            return True
        return False

def submit_case(user_info):
    submitted_by = user_info.submitted_by
    name = user_info.name
    age = user_info.age
    mobile = user_info.mobile
    father_name = user_info.father_name
    face_encoding = user_info.face_encoding
    image = user_info.image
    # image="hey"
    query = "insert into submitted_cases(submitted_by, name, father_name, age,\
             mobile, face_encoding, status, image) values('{}', '{}', '{}',\
             '{}', '{}', '{}', '{}', '{}')".format(submitted_by, name, father_name, age, mobile, face_encoding, "NF", image)
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
