import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

url = "https://b4d9364c-180b-4aab-8bee-4ae4a3dc7f6c-bluemix.cloudantnosqldb.appdomain.cloud"
# dealership_url = "https://b4d9364c-180b-4aab-8bee-4ae4a3dc7f6c-bluemix.cloudant.com/dashboard.html#database/dealerships/_all_docs"
# review_url = "https://b4d9364c-180b-4aab-8bee-4ae4a3dc7f6c-bluemix.cloudant.com/dashboard.html#database/reviews/_all_docs"
api_key = "Z3nL_AIQm9QkKuS2sE35a04Qz6tVgThIqx1BzZEFTlwI"


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key)
# def get_request(url):
#     response = requests.get(url, auth=HTTPBasicAuth('apikey', api_key))
#     return response.json()

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            # Basic authentication GET
            response = requests.get(
                url, 
                headers={'Content-Type': 'application/json'},
                params=kwargs,
                auth=HTTPBasicAuth('apikey', api_key))
        else:
            # no authentication GET
            response = requests.get(url, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
        return
    
    # status_code = response.status_code
    # print("With status {} ".format(status_code))
    json_data = response.json()
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
# def post_request(requests, url, payload, **kwargs):
#     return requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)
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

def get_dealer_by_id(url, id, **kwargs):
    results = []
    dealers = get_request(url, dealerId=id)
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

def get_dealers_by_state(url, state, **kwargs):
    results = []
    dealers = get_request(url, state=state)
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
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    dealer_reviews = get_request(url, dealer_id=dealer_id)
    if dealer_reviews:
        for review in dealer_reviews:
            if not "purchase_date" in review:
                purchase_date = "NA"
            else:
                purchase_date = review["purchase_date"]
            if not "car_make" in review:
                car_make = "NA"
            else:
                car_make = review["car_make"]
            if not "car_year" in review:
                car_year = "NA"
            else:
                car_year = review["car_year"]
            if not "car_model" in review:
                car_model = "NA"
            else:
                car_model = review["car_model"]
            review_obj = DealerReview(
                dealership = review["dealership"],
                name = review["name"],
                purchase = review["purchase"],
                purchase_date = purchase_date,
                car_make = car_make,
                car_model = car_model,
                car_year = car_year,
                sentiment = analyze_review_sentiments(review["review"]),
                review = review["review"],
                id = review["id"]
            )
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review):
    params = dict()
    params["text"] = dealer_review
    # params["version"] = kwargs["version"]
    params["features"] = {"sentiment":{}}
    # params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    response = requests.get(
        url,
        data=params,
        headers={'Content-Type': 'application/json'}, 
        auth=HTTPBasicAuth('apikey', api_key))
    try:
        return response.json()['sentiment']['document']['label']
    except KeyError:
        return "neutral"



