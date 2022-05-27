user_submission_table = """
    create table if not exists user_submissions
    (
        id varchar(64) not null
            constraint user_submissions_pk
                primary key,
        submitted_by varchar(64),
        face_encoding jsonb,
        location varchar(64) not null,
        mobile integer,
        image varchar(200000),
        status varchar(16),
        submitted_at timestamp
    )"""

submitted_cases_table = """
    create table if not exists submitted_cases
    (
        case_id varchar(64) not null primary key,
        submitted_by varchar(24) not null,
        name varchar(64) not null,
        father_name varchar(64) not null,
        age integer not null,
        mobile integer,
        face_encoding jsonb,
        image varchar(200000),
        submitted_on timestamp default CURRENT_TIMESTAMP not null,
        updated_on timestamp default CURRENT_TIMESTAMP not null,
        status varchar(24) not null
    )"""

users_tables = """
    create table if not exists users
    (
        username varchar(20) not null constraint users_pk primary key,
        password varchar(64) not null,
        role varchar(10) not null
    )"""

admin_user_query = (
    "insert into users(username, password, role) values('admin', 'admin', 'RW')"
)
