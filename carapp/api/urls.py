from django.conf.urls import url
from carapp.api.views import PopularAPIView

urlpatterns = [
    url("popular",PopularAPIView.as_view()),
]