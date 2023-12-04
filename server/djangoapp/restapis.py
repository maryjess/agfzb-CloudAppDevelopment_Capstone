import requests
import json
# import related models here
from .models import CarDealer
from requests.auth import HTTPBasicAuth

url = "https://b4d9364c-180b-4aab-8bee-4ae4a3dc7f6c-bluemix.cloudantnosqldb.appdomain.cloud"
api_key = "Z3nL_AIQm9QkKuS2sE35a04Qz6tVgThIqx1BzZEFTlwI"


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key)
def get_request(url):
    response = requests.get(url, auth=HTTPBasicAuth('apikey', api_key))
    return response.json()



# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
# def post_request(requests, url, payload, **kwargs):
#     return requests.post(url, params=kwargs, json=payload)
def post_request(url, json):
    response = requests.post(url, json=json)
    return response.json()


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    dealers = get_request(url)
    # print(response)
    if dealers:
        for dealer_doc in dealers:
            dealer_obj = CarDealer(
                address = dealer_doc["address"],
                city = dealer_doc["city"],
                full_name = dealer_doc["full_name"],
                id = dealer_doc["id"],
                lat = dealer_doc["lat"],
                long = dealer_doc["long"],
                short_name = dealer_doc["short_name"],
                st = dealer_doc["st"],
                zip = dealer_doc["zip"]
            )
            results.append(dealer_obj)
    return results



# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



