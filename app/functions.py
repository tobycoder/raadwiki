from app.authentication import raadzalen, raadzalen_afbeeldingen

def get_image_from_id(id="sdf"):
    data = raadzalen_afbeeldingen.where("rz_referentie", "==", "/raadzalen/" + id).limit(1).get()
    url = ""
    for x in data:
        url += x.to_dict()['image_url']
    return url
