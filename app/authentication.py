import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate(key)
fb = firebase_admin.initialize_app(cred)
db = firestore.client()
raadzalen = db.collection('raadzalen')
raadzalen_afbeeldingen = db.collection('raadzalen_afbeeldingen')
renovaties = db.collection('renovaties')