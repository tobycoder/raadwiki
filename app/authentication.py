import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
key = {
  "type": "service_account",
  "project_id": "raadzaalwiki",
  "private_key_id": "a8eac2ba13975424b47eef51ab9f5b8351128377",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCkpgQnqL1Itbvt\nxj+RRAvjqlgWvEon4fz2yideS2/oPW37rQYRGPEDSPatLzeEAyV6hpC5zqlXb6fi\n2Lt/koNUSGln0IzcAdzsmWfBwCHuF1c3xzsbJaZBNJcLNZig5G9cTWGKq+i3/c/u\nAvea+HoO4tRt1YTM41hn/yPc6VuzBDKRe1pidlQ7Qsw41oPzWh9yOkCCAFvjtG9b\nxoGn9WC7vgRD1qqxzOOfcihji35+LNmX9CrgIh47YBZUZGJbRMfkdO8TcWC/Kuo/\nK22prT6pJZHfN9lKHkchVj7HqXKBoaoBZADyor1wJh91RN0NcC0K+rBmu+xbxmTb\naw215fwHAgMBAAECggEAAhKY8Mrd/yFSiU66lCCQKcCGNVsPb+sXXR/0WOqIMRs8\n3DM0ZVi0B/+OI2X5w+6qNR2misBAP3qHWYKy8Ystngz/TrBAZbCcUFoqBTVe9/lR\nPsGCS/gwXJfF4v08u6HEiRvsQ2uglVhbmrps1YWVO8S9Odi7QD0Iat66W9iQL/Oz\nZ+f9Ox8ohX+/AsR0LHEARghywIAWoYoEHWtno0QF2oqZDn+mEr4UaqfnsfWGVaYU\neTBUt3cfx87rdqXWnCH6SUj8DRWy/slDDmYP14I+PgriK/34VtsHPQul3+/a6546\nqCdg+eAtuTO2CXCn/hnovzmjDcUj+8VZTJq4vzZsCQKBgQDP5hJXh7iXGEb6v+/h\nObh5nR1entdvg/cSdtqbqwFOv+3R1MOTP49SGwT9AcfszRqi732r0Tf4tP9QZC4V\nelNzPtoilYH42A8eG46iSTi//RvPbr7CenulLAUeRoDaxtawEGfiMiq9tyG/XBQo\nq1DjtV3VB7cMmEXV94k5SWr3KwKBgQDKvjdR8oODN2Fwf5VaxHAWdj8VGnF+VP0V\nFDyPNJpbCkHkhJOwnVM9gdgddd2LHxmfdQNnOmgNpw2HFLv2ALi5uWFJ1TUzACnP\nWPKses3wdu/wF66rMKVlbSEOA+FEa+30jCATMQ+NGlFBpE0eRZrVjLo/yHY2Di6d\nzJpZ39xglQKBgFzSn4vfOCaWG1LnkaXgzKHX6X4Os6fBpvXihTaNwnazsO5H7c53\nyXjiQXbpbacn6GWpQlYNgs0Tmw78u6qxREMnY+OfFznQ1ecebK++u4zU6K7UBm30\nm/IiVmKvHecQcliH6qoOthCgjHvRE9sYqnQQzUVJPYxtDHk9HVKrmgujAoGADyyH\nZWm6MBLwBwR1gDKdlQDKneC5x9PCkVZPZgRw3Ql6fwjxKNHNjhfuvd25dBUizM1s\nMMitSwBKweZqXvIU4Umfn3AGqEeF2Y/1sbULPskYEicjmopshpfRVoQx0vYk/B2U\ntPsCB/SFSl1qrC5XdU4wDmAJgOg00viiQMHBc7UCgYEAuJOihZpaiZ/Nx/xDkKLj\ntooA9svoFoIQFOa/H/pB9CkcO721rSLaeYHK0SSL3LEFYCWdvWbh0Q5V74FHwtOU\nDv/4JVCOcfqA2vLb+PynS83KMknTQYpiIg3/Id8LJiHjcaaKy5SSSZI93K+4DAaO\nDGN994UeMnqAixRi9Z+fktU=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-mun9y@raadzaalwiki.iam.gserviceaccount.com",
  "client_id": "112816993351674805751",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-mun9y%40raadzaalwiki.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

cred = credentials.Certificate(key)
fb = firebase_admin.initialize_app(cred)
db = firestore.client()
raadzalen = db.collection('raadzalen')
raadzalen_afbeeldingen = db.collection('raadzalen_afbeeldingen')