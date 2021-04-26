## functions to call zomato api for searching the restaurants
# get the API key from https://developers.zomato.com/documentation#/
import requests
import json

headers = {'user-key': '257cc9078e040a3cdbe9967179aa9e67',
           'Accept': 'application/json'}

def getLocationDetailsbyName(location_name):
    data = {'query': location_name}
    url = 'https://developers.zomato.com/api/v2.1/locations'
    data = requests.post(url, headers=headers, params=data)
    data = json.loads(data.text)
    print("Came to getLocationDetailsbyName ")
    print()

    if(len(data["location_suggestions"])>0):
        entity_type = data["location_suggestions"][0]["entity_type"]
        entity_id = data["location_suggestions"][0]["entity_id"]
        title = data["location_suggestions"][0]["title"]
        city_id=data["location_suggestions"][0]["city_id"]
        country_id=data["location_suggestions"][0]["country_id"]
        details={"restaurants_available":"yes","entity_type":entity_type,"entity_id":entity_id,"title":title,"city_id":city_id,"country_id":country_id}
        return details
    else:
        return {"restaurants_available":"no"}

def getLocationDetailsbyCoordinates(lat,lon):
    print("Came to getLocationDetailsbyCoordinates ")
    data = {'lat': lat,"lon":lon}
    url = 'https://developers.zomato.com/api/v2.1/geocode'
    data = requests.post(url, headers=headers, params=data)
    data = json.loads(data.text)

    if(len(data["location"])>0):
        entity_type = data["location"]["entity_type"]
        entity_id = data["location"]["entity_id"]
        title = data["location"]["title"]
        city_id= data["location"]["city_id"]
        country_id= data["location"]["country_id"]
        details={"restaurants_available":"yes","entity_type":entity_type,"entity_id":entity_id,"title":title,"city_id":city_id,"country_id":country_id}
        return details
    else:
         return {"restaurants_available":"no"}

def getLocationDetails(entity_id,entity_type):
    data = {'entity_id': entity_id,"entity_type":entity_type}
    url = 'https://developers.zomato.com/api/v2.1/location_details'
    data = requests.post(url, headers=headers, params=data)
    data = json.loads(data.text)
    top_cuisines = data["top_cuisines"]
    cuisines=[]

    for cuisine in top_cuisines:
        item={}
        item["title"] = cuisine
        item["payload"] = cuisine
        cuisines.append(item)

    best_restaurants=[]
    if(len(data["best_rated_restaurant"])<10):
        restoDataLen=len(data["best_rated_restaurant"])
    else:
        restoDataLen=10

    for i in range(0, restoDataLen):
        item={}
        photos=[]
        item["id"]=data["best_rated_restaurant"][i]["restaurant"]["id"]
        item["name"]=data["best_rated_restaurant"][i]["restaurant"]["name"]
        item["url"]=data["best_rated_restaurant"][i]["restaurant"]["url"]
        item["timings"]=data["best_rated_restaurant"][i]["restaurant"]["timings"]
        item["votes"]=data["best_rated_restaurant"][i]["restaurant"]["user_rating"]["votes"]
        item["image"]=data["best_rated_restaurant"][i]["restaurant"]["featured_image"]
        item["cuisines"]=data["best_rated_restaurant"][i]["restaurant"]["cuisines"]
        item["ratings"]=data["best_rated_restaurant"][i]["restaurant"]["user_rating"]["aggregate_rating"]
        item["rating_color"]=data["best_rated_restaurant"][i]["restaurant"]["user_rating"]["rating_color"]
        item["price_range"]=data["best_rated_restaurant"][i]["restaurant"]["price_range"]
        item["currency"]=data["best_rated_restaurant"][i]["restaurant"]["currency"]
        item["cost"]=data["best_rated_restaurant"][i]["restaurant"]["average_cost_for_two"]
        item["location"]=data["best_rated_restaurant"][i]["restaurant"]["location"]["locality_verbose"]
        item["user_rating_text"]=data["best_rated_restaurant"][i]["restaurant"]["user_rating"]["rating_text"]

        if "photos" in data["best_rated_restaurant"][i]["restaurant"].keys():
            if(len(data["best_rated_restaurant"][i]["restaurant"]["photos"])<5):
                photos_len=len(data["best_rated_restaurant"][i]["restaurant"]["photos"])
            else:
                photos_len=5
            for j in range(0,photos_len):
                photos.append(data["best_rated_restaurant"][i]["restaurant"]["photos"][j]["photo"]["url"])
            item["photos"]=photos
            best_restaurants.append(item)
        else:
            pass
        
    details={"top_cuisines":cuisines,"best_restaurants":best_restaurants}
    return details

def getCuisineId(cuisine_name,city_id):
    data = {'city_id': city_id}
    url = 'https://developers.zomato.com/api/v2.1/cuisines'
    data = requests.post(url, headers=headers, params=data)
    data = json.loads(data.text)
    # print("data: ",data)
    cuisines=data["cuisines"]
    cuisineID=None
    for cuisine in cuisines:
            if(cuisine_name.lower() == cuisine["cuisine"]["cuisine_name"].lower()):
                return cuisine["cuisine"]["cuisine_id"]
    return cuisineID

def searchRestaurants(entity_id,entity_type, cuisine_id,search_query):
    url = 'https://developers.zomato.com/api/v2.1/search'
    data = {"entity_id": entity_id, "entity_type": entity_type,
            "cuisines": cuisine_id, "count": "10","order":"asc"}
    data = requests.post(url, headers=headers, params=data)
    data = json.loads(data.text)
    restaurants=[]
    if(len(data["restaurants"])<10):
        restoDataLen=len(data["restaurants"])
    else:
        restoDataLen=10

    for i in range(0, restoDataLen):
        item={}
        photos=[]
        item["id"]=data["restaurants"][i]["restaurant"]["id"]
        item["name"]=data["restaurants"][i]["restaurant"]["name"]
        item["url"]=data["restaurants"][i]["restaurant"]["url"]
        item["timings"]=data["restaurants"][i]["restaurant"]["timings"]
        item["votes"]=data["restaurants"][i]["restaurant"]["user_rating"]["votes"]
        item["image"]=data["restaurants"][i]["restaurant"]["featured_image"]
        item["cuisines"]=data["restaurants"][i]["restaurant"]["cuisines"]
        item["ratings"]=data["restaurants"][i]["restaurant"]["user_rating"]["aggregate_rating"]
        item["rating_color"]=data["restaurants"][i]["restaurant"]["user_rating"]["rating_color"]
        item["price_range"]=data["restaurants"][i]["restaurant"]["price_range"]
        item["cost"]=data["restaurants"][i]["restaurant"]["average_cost_for_two"]
        item["location"]=data["restaurants"][i]["restaurant"]["location"]["locality_verbose"]
        item["currency"]=data["restaurants"][i]["restaurant"]["currency"]
        item["user_rating_text"]=data["restaurants"][i]["restaurant"]["user_rating"]["rating_text"]

        if "photos" in data["restaurants"][i]["restaurant"].keys():
            if(len(data["restaurants"][i]["restaurant"]["photos"])<5):
                photos_len=len(data["restaurants"][i]["restaurant"]["photos"])
            else:
                photos_len=5
            for j in range(0,photos_len):
                photos.append(data["restaurants"][i]["restaurant"]["photos"][j]["photo"]["url"])
            item["photos"]=photos
            restaurants.append(item)
        else:
            pass
        
   
    return restaurants
