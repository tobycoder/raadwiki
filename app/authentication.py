import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from app.extensions import key
from google.cloud import storage
import os




cred = credentials.Certificate(key)
fb = firebase_admin.initialize_app(cred)
db = firestore.client()
raadzalen = db.collection('raadzalen')
raadzalen_afbeeldingen = db.collection('raadzalen_afbeeldingen')
renovaties = db.collection('renovaties')
messages = db.collection('messages')
replies = db.collection('reply')