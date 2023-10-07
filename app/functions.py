from app.authentication import raadzalen, raadzalen_afbeeldingen
from flask import session
def get_image_from_id(id="sdf"):
    data = raadzalen_afbeeldingen.where("rz_referentie", "==", "/raadzalen/" + id).limit(1).get()
    url = ""
    for x in data:
        url += x.to_dict()['image_url']
    return url

def login_check():
    if session['user']:
        return True
    else:
        return False