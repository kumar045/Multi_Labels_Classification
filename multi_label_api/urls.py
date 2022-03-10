from django.conf.urls import url
from .views import *
from django.urls import path

urlpatterns = [
    url(r'^image_upload/$', RoadDetectionAPIView.as_view(), name='image_upload'),


]