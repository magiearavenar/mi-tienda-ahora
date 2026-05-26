from django.urls import path
from .feed import google_feed_xml

urlpatterns = [
    path('feed/google-shopping.xml', google_feed_xml, name='google_feed'),
]
