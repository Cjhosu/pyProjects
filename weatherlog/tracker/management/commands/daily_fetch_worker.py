from django.conf import settings
from django.core.management.base import BaseCommand
from ...views.darksky_views import CurrentWeather
from ...models import Location
import requests
from datetime import date, datetime, timedelta

darkskykey = settings.DARK_SKY_KEY
yesterday = datetime.now() - timedelta(days=1)
yest = yesterday.strftime('%s')

class Command(BaseCommand):

    url = 'https://api.darksky.net/forecast/'+darkskykey+'/'
    help = "Fetches weatherdate for a location on a schedule."

    def add_arguments(self, parser):
        parser.add_argument('--location')

    def getLocation(self,current):
        home_location = Location.objects.get(locality_name = current)
        latitude = str(home_location.latitude)
        longitude = str(home_location.longitude)
        response = requests.get(self.url+latitude+','+longitude+','+yest+'?exclude=minutely,currently,hourly,alerts,flags')
        weatherdata = response.json()
        uv_index = weatherdata["daily"]["data"][0]["uvIndex"]
        return uv_index


    def handle(self,*args, **options):
        current = options['location']
        home_location = self.getLocation(current)
        print (home_location)
