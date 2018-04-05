#!/usr/bin/python3
from urllib import request
import json


def check():
    try:
        api_key = ""
        wunderground = "http://api.wunderground.com/api/"
        geo_lookup = "/geolookup/conditions/q/"
        loc = input("location: ")
        query_url = wunderground+api_key+geo_lookup+loc+".json"
        main(query_url)
    except(ValueError):
        print("Bad location! Try again!")
        check()


def main(query_url):
    try:
        f = request.urlopen(query_url)

        f_read = f.read()
        f_read_decode = f_read.decode('utf-8')  # deocode the bytes obj to str
        data = json.loads(f_read_decode)  # deserialize the str obj to dict obj
        location = data['location']['city']
        temp_c = data['current_observation']['temp_c']
        print("Current temperature in {city} is: {temp} C"
              .format(city=location, temp=temp_c))
    except(ValueError, KeyError):
        print("Something went wrong. Try again")
        check()


if __name__ == "__main__":
    check()
