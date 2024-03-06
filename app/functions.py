from app.authentication import raadzalen, raadzalen_afbeeldingen, renovaties
from flask import session
from google.cloud import firestore
from google.cloud.firestore_v1 import aggregation
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime, timedelta
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

def count_raadzalen_by_user(email):
    """Builds an aggregate query that returns the number of results in the query.

    Arguments:
      project_id: your Google Cloud Project ID
    """
    query = raadzalen.where(filter=FieldFilter("auteur", "==", email))
    aggregate_query = aggregation.AggregationQuery(query)

    # `alias` to provides a key for accessing the aggregate query results
    aggregate_query.count(alias="all")

    results = aggregate_query.get()
    for result in results:
        print = result[0].value

    return print
def count_renovaties_by_user(email):
    """Builds an aggregate query that returns the number of results in the query.

    Arguments:
      project_id: your Google Cloud Project ID
    """
    query = renovaties.where(filter=FieldFilter("auteur", "==", email))
    aggregate_query = aggregation.AggregationQuery(query)

    # `alias` to provides a key for accessing the aggregate query results
    aggregate_query.count(alias="all")

    results = aggregate_query.get()
    for result in results:
        print = result[0].value

    return print

def count_entries(collection):
    query = collection.order_by("auteur")
    aggregate_query = aggregation.AggregationQuery(query)
    aggregate_query.count(alias="all")
    results = aggregate_query.get()

    for result in results:
        print = result[0].value

    return print

def count_entries_query(query):
    aggregate_query = aggregation.AggregationQuery(query)
    aggregate_query.count(alias="all")
    results = aggregate_query.get()

    for result in results:
        print = result[0].value

    return print