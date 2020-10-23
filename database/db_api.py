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
    case_id = user_info.case_id
    query = f"insert into submitted_cases(submitted_by, name, father_name, age,\
             mobile, face_encoding, status, image, case_id) values('{submitted_by}', '{name}', '{father_name}',\
             '{age}', '{mobile}', '{face_encoding}', 'NF', '{image}', '{case_id}')"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)


def get_train_data(submitted_by):
    query = "select case_id, face_encoding from submitted_cases where submitted_by='{}' and status='NF'".format(submitted_by)
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def submit_user_data(user_submission):
    name = user_submission.name
    location = user_submission.location
    mobile = user_submission.mobile
    image = user_submission.image
    face_encoding = user_submission.face_encoding
    sub_id = user_submission.sub_id
    status = 'NC'
    query = f"insert into user_submissions(id, submitted_by, face_encoding,\
              location, mobile, image, status) values('{sub_id}', '{name}', '{face_encoding}',\
              '{location}', '{mobile}', '{image}', 'NR')"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)


def get_user_submission(status='NR'):
    query = f"select id, face_encoding from user_submissions where status='{status}'"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def get_case_details(case_id):
    query = f"select name, father_name, image, mobile, age from submitted_cases where case_id={case_id}"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def get_user_details(case_id):
    query = f"select location, date, image from user_submissions where id={case_id}"
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
