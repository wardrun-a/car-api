from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework import status
from .serializers import *
from .models import *
import requests


url="https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForVehicleType/car?format=json"

response = requests.get(url).json()
items = list(response.items())
result=items[-1][1]
idlist=[]
for i in result:
    data = i['MakeId']
    idlist.append(data)

makelist=[]
for k in idlist:
    URL = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/{k}?format=json"
    responses = requests.get(URL).json()
    makelist.append(responses)

cardetails = []
for j in makelist:
    carlist = list(j.items())
    makenmodel = carlist[-1][1]
    cardetails.append(makenmodel)

make_model_dic = {}
model = []
for datas in cardetails:
    for data in datas:
        model.append(data['Model_Name'])

    make_model_dic[data['Make_Name']] = model
    model=[]



@api_view()
@permission_classes([AllowAny])
def firstFunction(request):
    return Response({"Message":"EndPoints is 'cars'(for POST and GET), 'rate', 'popular'."})

class CarViewsets(viewsets.ModelViewSet):
    serializer_class = CarSerializer

    def get_queryset(self):
        cars = Car.objects.all()
        return cars

    def create(self,request,*args,**kwargs):
        car_data = request.data
        for k in make_model_dic.keys():
            if k == car_data["make"].upper():
                cars = make_model_dic[k]                
                model_lower = car_data["model"].lower()
                model_in_list = model_lower in (model.lower() for model in cars)
                if model_in_list:
                    details = Car.objects.create(make=k,model=car_data["model"].title())
                    details.save()                    
                    post = {
                        "make": k,
                        "model": car_data["model"].title()
                    }

                    return Response(post)     
            
        return Response({'message': 'There is no such Car'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self,request,*args,**kwargs):
        try: 
            car = self.get_object()
            car.delete()
            return Response({"Message": "Deletion Successfull!"})
        except Car.DoesNotExist:         
            return Response({'message': 'There is no such Data'}, status=status.status.HTTP_404_NOT_FOUND)



class RatingViewsets(viewsets.ModelViewSet):
    serializer_class = RatingSerializer

    def get_queryset(self):
        rating = Rating.objects.all()
        return rating

    def create(self,request,*args,**kwargs):
        rate_number=1
        sum_of_max_rating = 0
        sum_of_raters = 0
        try:
            rating_data = request.data
            rating = Rating.objects.all()
            car_data=Car.objects.get(pk=rating_data["car_id"])
            details = Rating.objects.create(car_id=rating_data["car_id"],rating=rating_data["rating"])
            details.save()
            car_data.rates_number = rate_number + car_data.rates_number
            serializer = RatingSerializer(details)
            for i in rating:
                if int(rating_data["car_id"])==int(i.car_id):
                    sum_of_max_rating += i.rating
                    sum_of_raters += 1
            sum_of_max_rating_of_user_count = sum_of_raters * 5
            avg_of_rating = (sum_of_max_rating*5) / sum_of_max_rating_of_user_count
            car_data.avg_rating = "{:.2f}".format(avg_of_rating)
            car_data.save()

            # to avoid csrfmiddlewaretoken displaying in output
            post= {
                "car_id": rating_data["car_id"],
                "rating": rating_data["rating"]
            }
            return Response(post)
        except Car.DoesNotExist:
            return Response({'message': 'There is no car in that Id!'}, status=status.HTTP_204_NO_CONTENT)



        
