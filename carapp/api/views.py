from rest_framework.views import APIView
from rest_framework.response import Response
from carapp.api.serializers import *
from carapp.models import *

class PopularAPIView(APIView):
    serializer = PopularSerializer

    def get_queryset(self):
        cars = Car.objects.all()
        return cars

    def get(self,request,*args,**Kwargs):
        cars = self.get_queryset()
        serializer = PopularSerializer(cars, many=True)
        return Response(serializer.data)