from urllib import request
import json
from django.db.models import Count
from app.models import View, Post
from taggit.models import Tag

def view_log(model):
    try:
        with request.urlopen("https://geoip-db.com/json/") as url:
            data = json.loads(url.read().decode())
            ip = data['IPv4'] or data['IPv6']
            view_log = View.objects.create(ip=ip, state=data['state'], city=data['city'], country_name=data['country_name'], country_code=data['country_code'], latitude=data['latitude'], longitude=data['longitude'])
            model.views.add(view_log)
            model.save()
    except:
        print("ViewLogError: Sorry couldn't save view log to database")

def view_log_entry(model, data):
    ip = data['IPv4'] or data['IPv6']
    view_log = View.objects.create(ip=ip, state=data['state'], city=data['city'], country_name=data['country_name'], country_code=data['country_code'], latitude=data['latitude'], longitude=data['longitude'])
    model.views.add(view_log)
    model.save()


def ip_info():
    try:
        with request.urlopen("https://geoip-db.com/json/") as url:
            print('From GEO-IP')
            return json.loads(url.read().decode())
    except:
        print("IPData: Couldn't get ip location information")

def get_tags():
    return Post.tags.most_common_public()[:5]
