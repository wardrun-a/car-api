from django.db import models

# Create your models here.
class Car(models.Model):
    id = models.AutoField(primary_key=True)
    make = models.CharField(max_length=225)
    model = models.CharField(max_length=225)
    avg_rating = models.FloatField(default=0,blank=True, null=True)
    rates_number = models.IntegerField(default=0,blank=True, null=True)

    def __str__(self):
        return self.make

class Rating(models.Model):
    car_id = models.IntegerField()
    rating = models.FloatField()

    def __str__(self):
        return str(self.car_id)

