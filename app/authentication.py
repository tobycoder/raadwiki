import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate('app/key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
raadzalen = db.collection('raadzalen')
raadzalen_afbeeldingen = db.collection('raadzalen_afbeeldingen')