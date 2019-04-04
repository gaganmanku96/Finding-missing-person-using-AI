import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://missing-person-e1a61.firebaseio.com'
})

print('Connection to DB established')