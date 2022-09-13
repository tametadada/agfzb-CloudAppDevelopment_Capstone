from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .restapis import *
from .models import CarModel, CarMake, CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, get_request, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
from django.db import models
from django.core import serializers
from django.utils.timezone import now
import uuid
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html',context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
    if user is not None:
        login(request,user)
        return redirect('djangoapp:index')
    else:
        return render(request, 'djangoapp/registration.html')


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exists = False
        try:
            User.objects.get(username=username)
            user_exists = True
        except:
            print('{} user name is taken'.format(username))

    if not user_exists:
        user = User.objects.create_user(username=username, first_name=first_name,
            last_name=last_name, password=password)
        login(request, user)

        return redirect('djangoapp:index')
    else:
        return render(request, 'djangoapp/registration.html')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://fb426293.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context['dealerships'] = dealerships
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer

def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://fb426293.us-south.apigw.appdomain.cloud/api/dealership"
        # dealer = get_dealers_from_cf(dealer_url, id=id)
        dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        
        context["dealer"] = dealer

        review_url = "https://fb426293.us-south.apigw.appdomain.cloud/api2/review"
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        print(reviews)
        context["reviews"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)
        
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

def add_review(request, id):
    if request.user.is_authenticated:
        context = {}
        dealer_url = "https://fb426293.us-south.apigw.appdomain.cloud/api/dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, id)
        context["dealer"] = dealer
        if request.method == "GET":
            cars = CarModel.objects.all()
            context["cars"] = cars
            print(context)
            return render(request, 'djangoapp/add_review.html', context)
        
        if request.method == "POST":
            review = {}
            review["name"] = request.user.first_name + " " + request.user.last_name
            form = request.POST
            review["dealership"] = id
            review["review"] = form["content"]
            if(form.get("purchasecheck") == "on"):
                review["purchase"] = True
            else:
                review["purchase"] = False
            if(review["purchase"]):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
                car = CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.make.name
                review["car_model"] = car.name
                review["car_year"] = car.year
            post_url = "https://fb426293.us-south.apigw.appdomain.cloud/api2/review"
            json_payload = { "review": review }
            post_request(post_url, json_payload, id=id)
            return redirect("djangoapp:dealer_details", id=id)
    else:
        return redirect("/djangoapp/login")
