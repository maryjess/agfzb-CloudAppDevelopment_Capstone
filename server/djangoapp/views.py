from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarModel
from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('/djangoapp')
        return render(request, 'djangoapp/login.html', context)
    return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    context = {}
    print(f"Log out the user {request.user.username}")
    logout(request)
    return redirect('/djangoapp')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == "POST":
        user_exist = False
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug(f"{username} is a new user")
        if not user_exist:
            user = User.objects.create_user(
                username = username, 
                password = password,
                first_name = first_name,
                last_name = last_name)
            login(request, user = user)
            return redirect("/djangoapp")
        return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     url = "http://localhost:3000/dealerships/get"
#     context = {
#         "dealerships": get_dealers_from_cf(url)
#     }
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)

def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "http://localhost:3000/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Return a list of dealer short name
        context = { "dealerships": dealerships }
        return render(request, "djangoapp/index.html", context = context)


# def get_dealerships_by_id(request, id):
#     context = {}
#     if request.method == "GET":
#         url = "http://localhost:3000/dealerships/get"
#         # Get dealers from the URL
#         dealerships = get_dealerships_by_id(url, id = id)
#         # Return a list of dealer short name
#         context = { "dealerships": dealerships }
#         return render(request, "djangoapp/index.html", context = context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "http://localhost:8080/reviews/get"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context = { "reviews": reviews }
        # reviews_string = ' '.join([review.sentiment for review in reviews])
        return render(request, 'djangoapp/dealer_details.html', context = context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "GET":
        url = "http://localhost:3000/dealerships/get"
        dealer = get_dealers_from_cf(url)[0]
        context = {
            "cars": CarModel.objects.all(),
            "dealer": dealer,
            "dealer_id": dealer_id
        }
        return render(request, 'djangoapp/add_review.html', context = context)
    
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('/djangoapp')

        car = CarModel.objects.get(pk = request.POST['car'])
        review = dict()
        review["dealership"] = dealer_id
        review["purchase_check"] = request.POST['purchase_check']
        if request.POST['purchase_check']:
            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime("%Y")
            review["purchase_date"] = request.POST['purchase_date'].isoformat()
        else:
            review["car_make"] = ''
            review["car_model"] = ''
            review["car_year"] = ''
            review["purchase_date"] = ''
        review["review"] = request.POST['content']
        review["name"] = f"{user.first_name} {user.last_name}"
        
        json_payload = {"review": review}
        url = "https://b4d9364c-180b-4aab-8bee-4ae4a3dc7f6c-bluemix.cloudantnosqldb.appdomain.cloud"
        post_request(url, json_payload, dealer_id = dealer_id)
        return redirect('djangoapp:dealer_details', dealer_id = dealer_id)
    
# def add_review(request, dealer_id):
#     if request.method == "GET":
#         url = f"https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/a9220b6d6b26f1eb3b657a98770b743616f7d4cd223b89cd1ca4e88ab49bdb92/api/dealership?dealerId={dealer_id}"
#         # Get dealers from the URL
#         context = {
#             "cars": CarModel.objects.all(),
#             "dealer": get_dealers_from_cf(url)[0],
#         }
#         print(context)
#         return render(request, 'djangoapp/add_review.html', context)
    # if request.method == "POST":
    #     if form.get("purchasecheck"):
    #         review["purchasedate"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
    #         car = CarModel.objects.get(pk=form["car"])
    #         review["car_make"] = car.car_make.name
    #         review["car_model"] = car.name
    #         review["car_year"]= car.year.strftime("%Y")
    #     json_payload = {"review": review}
    #     URL = 'https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/a9220b6d6b26f1eb3b657a98770b743616f7d4cd223b89cd1ca4e88ab49bdb92/api/review'
    #     post_request(URL, json_payload, dealerId=dealer_id)
    # return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

