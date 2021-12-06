from rest_framework import serializers
from carapp.models import *

class PopularSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id","make","model","rates_number"]