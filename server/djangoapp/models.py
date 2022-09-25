from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core import serializers 
import uuid
import json

# Create your models here.

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=100)
    description = models.CharField(null=False, max_length=500)

    def __str__(self):
        return 'Name:' + self.name + ',' + \
            'Description:' + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    
    CarType = (
        ('CPE', 'COUPE'),
        ('PKU', 'PICKUP'),
        ('SDN', 'SEDAN'),
        ('SUV', 'SUV'),
        ('WGN', 'WAGON')
    )

    
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=60)
    id = models.IntegerField(null=False, primary_key=True)
    car_type = models.CharField(null=False, choices=CarType, max_length=25)
    year = models.PositiveSmallIntegerField(null=False, validators=[MinValueValidator(1900)])
    
    def __str__(self):
        return 'Name ' + self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review):
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = ""
        self.car_make = ""
        self.car_model = ""
        self.car_year = ""
        self.sentiment = ""
        self.id = ""

    def __str__(self):
        return "Reviewer name: " + self.name + " Review: " + self.review

# postReview
class ReviewPost:

    def __init__(self, dealership, name, purchase, review):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = ""
        self.car_make = ""
        self.car_model = ""
        self.car_year = ""

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)