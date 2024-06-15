import firebase_admin
from firebase_admin import firestore
from google.auth import exceptions



# database connection
def connect_database():
    db: firestore.client = None
    cred = None
    try:
        cred = firebase_admin.credentials.Certificate("class_database/certs/lossotoys-key.json")
    except FileNotFoundError:
        db = "Cert file don't exist"
    finally:
        firebase_admin.initialize_app(cred)
        db = firestore.client()
    return db


