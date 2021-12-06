from rest_framework import serializers
from carapp.models import *

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id","make","model","avg_rating"]



class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["car_id","rating"]