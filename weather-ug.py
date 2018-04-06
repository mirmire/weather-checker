#!/usr/bin/python3
from urllib import request
import json


def main():
    """Main function asks the user for the location
       and tries to do basic cleaning"""
    try:
        location = input("location: ")
        city, country = location.split()
        city = city.strip()
        country = country.strip()
        underground(country, city)
        google(country, city)
    except(ValueError):
        print("Use city country format like : oulu finland")
        main()


def underground(country, city):
    """"Make API call to the Weather Underground endpoint
        and extract weather data """
    # splitting up query parts makes it modular and short neat lines
    try:
        location = "{country}/{city}".format(country=country, city=city)
        api_key = ""
        w_url = "http://api.wunderground.com/api/"
        geo_lookup = "/geolookup/conditions/q/"
        query_url = w_url+api_key+geo_lookup+location+".json"

        data = clean_data(query_url)  # send the query and get back dictionary
        location = data['location']['city']

        # temp_c can be changed to temp_f for different unit
        temp = data['current_observation']['temp_c']
        feels_like = data['current_observation']['feelslike_c']
        sky = data['current_observation']['weather']
        print_summary("WUNDERGROUND", temp, feels_like, sky)
    except(ValueError):
        print("Something went wrong. Try again!")
        main()


def google(country, city):
    """Google is needed to find the longitude and latitude of given location"""
    try:
        location = "{city}+{country}".format(country=country, city=city)
        g_url = "https://maps.googleapis.com/maps/api/geocode/json?address="
        api_key = ""
        query_string = g_url+location+"&key="+api_key
        data = clean_data(query_string)
        longitude = data['results'][0]['geometry']['location']['lng']
        latitude = data['results'][0]['geometry']['location']['lat']
        dark_sky(latitude, longitude)
    except(ValueError):
        print("Something went wrong. Try again!")
        main()


def dark_sky(lat, lng):
    dark_sky_url = "https://api.darksky.net/forecast/"
    api_key = ""
    query_string = dark_sky_url+api_key+"/{lat},{lng}?units=si"\
        .format(lat=lat, lng=lng)
    data = clean_data(query_string)
    temp = data['currently']['temperature']
    feels_like = data['currently']['apparentTemperature']
    sky = data['currently']['summary']
    print_summary("DARK SKY", temp, feels_like, sky)


def clean_data(query_url):
    """Make function call with the passed query string and parse the output"""
    try:
        f = request.urlopen(query_url)

        f_read = f.read()
        f_read_decode = f_read.decode('utf-8')  # deocode the bytes obj to str
        data = json.loads(f_read_decode)  # deserialize the str obj to dict obj
        return data
    except(ValueError, KeyError):
        print("Something went wrong. Try again")
        main()


def print_summary(source, temp, feels_like, sky):
    print("{source} : {temp} C, Feels like : {feel} C, Weather: {sky}"
          .format(source=source, temp=temp, feel=feels_like, sky=sky))


if __name__ == "__main__":
    print("Type the location to get weather information in "
          "city country format.")
    main()
