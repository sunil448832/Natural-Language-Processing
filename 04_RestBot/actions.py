# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet,UserUtteranceReverted
from rasa_sdk.forms import FormAction
import zomatoApi
import json

class ActionGreetUser(Action):
    """
    Greet user for the first time he has opened the bot windows
    """
    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_greet_user")   
        return [UserUtteranceReverted()] 

class ActionShowMoreRestaurants(Action):
    """
    Show more results of the restaurants
    """
    def name(self) -> Text:
        return "action_show_more_results"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        restaurants = tracker.get_slot("more_restaurants")
        if restaurants!=None:
            if(tracker.get_latest_input_channel()=="slack"):
                restData = getResto_Slack(restaurants,show_more_results=False)
                dispatcher.utter_message(text="Here are few more restaurants",json_message=restData)
            else:
                dispatcher.utter_message(text="Here are few more restaurants",json_message={"payload":"cardsCarousel","data":restaurants})
            
            return [SlotSet("more_restaurants", None)] 
        else:
            dispatcher.utter_message(text="Sorry No more restaurants found")
            return []
        

class ActionSearchRestaurants(Action):
    """
    Search the restaurants using location & cuisine.

    Required Parameters: Location, Cuisine
    """
    def name(self) -> Text:
        return "action_search_restaurants"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print()
        print("====Inside ActionSearchRestaurants====")
        print()

        ## extract the required slots
        location=tracker.get_slot("location")
        cuisine=tracker.get_slot("cuisine")
        lat=tracker.get_slot("latitude")
        lon=tracker.get_slot("longitude")
        entity_id=tracker.get_slot("location_id")
        entity_type=tracker.get_slot("location_type")
        city_id=tracker.get_slot("city_id")

        ## extract the entities
        locationEntity=next(tracker.get_latest_entity_values("location"), None)
        cuisineEntity=next(tracker.get_latest_entity_values("cuisine"), None)
        user_locationEntity=next(tracker.get_latest_entity_values("user_location"), None)
        latEntity=next(tracker.get_latest_entity_values("latitude"), None)
        lonEntity=next(tracker.get_latest_entity_values("longitude"), None)

        ## if we latitude & longitude entities are found, set it to slot
        if(latEntity and lonEntity):
            lat=latEntity
            lon=lonEntity
        
        ## if user wants to search restaurants in his current location
        if(user_locationEntity or (latEntity and lonEntity) ):
            ##check if we already have the user location coordinates stoed in slots
            if(lat==None and lon==None):
                dispatcher.utter_message(text="Sure, please allow me to access your location 🧐",json_message={"payload":"location"})
                
                return []
            else:
                locationEntities=zomatoApi.getLocationDetailsbyCoordinates(lat,lon)
                location=locationEntities["title"]
                city_id=locationEntities["city_id"]
                entity_id=locationEntities["entity_id"]
                entity_type=locationEntities["entity_type"]
                
                ## store the user provided details to slot
                SlotSet("location", locationEntities["title"])
                SlotSet("city_id", locationEntities["city_id"])
                SlotSet("location_id", locationEntities["entity_id"])
                SlotSet("location_type", locationEntities["entity_type"])

        ## if user wants to search restaurants by location name
        if(locationEntity):
            locationEntities=zomatoApi.getLocationDetailsbyName(locationEntity)
            if(locationEntities["restaurants_available"]=="no"):
                dispatcher.utter_message("Sorry I couldn't find any restaurants  😓")
                return []
            entity_id=locationEntities["entity_id"]
            entity_type=locationEntities["entity_type"]
            city_id=locationEntities["city_id"]
            SlotSet("location", locationEntities["title"])

        ##get the cuisine id for the cuisine name user provided
        cuisine_id=zomatoApi.getCuisineId(cuisine,city_id)
        
        print("Entities:  ",entity_id," ",entity_type," ",cuisine_id," ",location," ",cuisine)
        print()

        ## if we didn't find the restaurant for which user has provided the cuisine name
        if(cuisine_id==None):
            dispatcher.utter_message("Sorry we couldn't find any restaurants that serves {} cuisine in {}".format(cuisine,location))
            return [UserUtteranceReverted()] 
        else:
            ## search the restaurts by calling zomatoApi api
            restaurants=zomatoApi.searchRestaurants(entity_id,entity_type, cuisine_id,"")

            ## check if restaurants found
            if(len(restaurants)>0):

                if(tracker.get_latest_input_channel()=="slack"):
                    more_restaurants=[]
                    if(len(restaurants)>5):
                        restData=getResto_Slack(restaurants[:5],show_more_results=True)
                        more_restaurants=restaurants[5:]
                    else:
                        restData=getResto_Slack(restaurants,show_more_results=False)

                    dispatcher.utter_message(text="Here are the few restaurants that matches your preferences 😋",json_message=restData)
                    return [SlotSet("more_restaurants", more_restaurants)]    
                else:
                    if(len(restaurants)>5):   
                        dispatcher.utter_message(text="Here are the few restaurants that matches your preferences 😋",json_message={"payload":"cardsCarousel","data":restaurants[:5]})
                        return [SlotSet("more_restaurants", restaurants[5:])]
                    else:
                        dispatcher.utter_message(text="Here are the few restaurants that matches your preferences 😋",json_message={"payload":"cardsCarousel","data":restaurants})
                        return [SlotSet("more_restaurants", None)]    
            
            else:    
                dispatcher.utter_message("Sorry we couldn't find any restaurants that serves {} cuisine in {} 😞".format(cuisine,location))
                return [UserUtteranceReverted()] 
            
           
class ActionSearchBestRestaurants(Action):
    """
    Search the best restaurants using location.
    
    Required Parameters: Location
    """
    def name(self) -> Text:
        return "action_search_best_restaurants"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print()
        print("======Inside Action Search Best Restaurants====")
        print()

        ## extract the required slots
        location=tracker.get_slot("location")
        cuisine=tracker.get_slot("cuisine")
        lat=tracker.get_slot("latitude")
        lon=tracker.get_slot("longitude")
        entity_id=tracker.get_slot("location_id")
        entity_type=tracker.get_slot("location_type")
        city_id=tracker.get_slot("city_id")

        ## extract the entities
        locationEntity=next(tracker.get_latest_entity_values("location"), None)
        cuisineEntity=next(tracker.get_latest_entity_values("cuisine"), None)
        user_locationEntity=next(tracker.get_latest_entity_values("user_location"), None)
        latEntity=next(tracker.get_latest_entity_values("latitude"), None)
        lonEntity=next(tracker.get_latest_entity_values("longitude"), None)

        ## if we latitude & longitude entities are found, set it to slot
        if(latEntity and lonEntity):
            lat=latEntity
            lon=lonEntity

        ## if user wants to search the best restaurants in his current location
        if(user_locationEntity or (latEntity and lonEntity) ):
            ##check if we already have the user location coordinates stoed in slots
            if(lat==None and lon==None):
                dispatcher.utter_message(text="Sure, please allow me to access your location 🧐",json_message={"payload":"location"})
              
                return []
            else:
                locationEntities=zomatoApi.getLocationDetailsbyCoordinates(lat,lon)
                location=locationEntities["title"]
                city_id=locationEntities["city_id"]
                entity_id=locationEntities["entity_id"]
                entity_type=locationEntities["entity_type"]
                
                ## store the user provided details to slot
                SlotSet("location", locationEntities["title"])
                SlotSet("city_id", locationEntities["city_id"])
                SlotSet("location_id", locationEntities["entity_id"])
                SlotSet("location_type", locationEntities["entity_type"])

        ## if user wants to search best restaurants by location name
        if(locationEntity):
            locationEntities=zomatoApi.getLocationDetailsbyName(locationEntity)
            entity_id=locationEntities["entity_id"]
            entity_type=locationEntities["entity_type"]
            city_id=locationEntities["city_id"]

        print("Entities: ",entity_id," ",entity_type," ",city_id," ",locationEntity)
        
        ## search the best restaurts by calling zomatoApi api
        restaurants=zomatoApi.getLocationDetails(entity_id,entity_type)

        
        if(len(restaurants)>0):
            if(tracker.get_latest_input_channel()=="slack"):
                more_restaurants=None
                if len(restaurants["best_restaurants"])>5:
                    restData=getResto_Slack(restaurants["best_restaurants"][:5],show_more_results=True)
                    more_restaurants=restaurants["best_restaurants"][5:]
                    dispatcher.utter_message(text="Here are few top rated restaurants that I have found 🤩",json_message=restData)
                else:
                    restData=getResto_Slack(restaurants["best_restaurants"],show_more_results=False)

                    dispatcher.utter_message(text="Here are few top rated restaurants that I have found 🤩",json_message=restData)
                return [SlotSet("more_restaurants", more_restaurants)]    
            else:
                if len(restaurants["best_restaurants"])>5:
                    dispatcher.utter_message(text="Here are few top rated restaurants that I have found 🤩",json_message={"payload":"cardsCarousel","data":restaurants["best_restaurants"][:5]})
                    return [SlotSet("more_restaurants", restaurants["best_restaurants"][5:])]    
                else:
                    dispatcher.utter_message(text="Here are few top rated restaurants that I have found 🤩",json_message={"payload":"cardsCarousel","data":restaurants["best_restaurants"]})
                    return [SlotSet("more_restaurants", None)]    
        else:    
            dispatcher.utter_message("Sorry we couldn't find any restaurants that serves {} cuisine in {} 😞".format(cuisine,location))
            return [UserUtteranceReverted()] 
        

class ActionSearchRestaurantsWithoutCuisine(Action):
    """
    Search the best restaurants using location and user is fine with any cuisine.
    
    Required Parameters: Location
    """
    def name(self) -> Text:
        return "action_search_restaurants_without_cuisine"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("====Inside ActionSearchRestaurants Without Cuisine====")
        print()
        location=tracker.get_slot("location")
        cuisine=tracker.get_slot("cuisine")
        lat=tracker.get_slot("latitude")
        lon=tracker.get_slot("longitude")
        entity_id=tracker.get_slot("location_id")
        entity_type=tracker.get_slot("location_type")
        city_id=tracker.get_slot("city_id")

        locationEntity=next(tracker.get_latest_entity_values("location"), None)
        cuisineEntity=next(tracker.get_latest_entity_values("cuisine"), None)
        user_locationEntity=next(tracker.get_latest_entity_values("user_location"), None)
        
        ##set the cuisine to any of the cuisine name or you leave it empyt
        cuisine_id=""
        restaurants=zomatoApi.searchRestaurants(entity_id,entity_type, cuisine_id,"")
        
        ## check if restaurants found
        if(len(restaurants)>0):

            if(tracker.get_latest_input_channel()=="slack"):
                more_restaurants=[]
                if(len(restaurants)>5):
                    restData=getResto_Slack(restaurants[:5],show_more_results=True)
                    more_restaurants=restaurants[5:]
                else:
                    restData=getResto_Slack(restaurants,show_more_results=False)

                dispatcher.utter_message(text="Here are the few restaurants that matches your preferences 😋",json_message=restData)
                return [SlotSet("more_restaurants", more_restaurants)]    
            else:
                if(len(restaurants)>5):   
                    dispatcher.utter_message(text="Here are the few restaurants that matches your preferences 😋",json_message={"payload":"cardsCarousel","data":restaurants[:5]})
                    return [SlotSet("more_restaurants", restaurants[5:])]
                else:
                    dispatcher.utter_message(text="Here are the few restaurants that matches your preferences 😋",json_message={"payload":"cardsCarousel","data":restaurants})
                    return [SlotSet("more_restaurants", None)]    
        
        else:    
            dispatcher.utter_message("Sorry we couldn't find any restaurants that serves {} cuisine in {} 😞".format(cuisine,location))
            return [UserUtteranceReverted()] 

class ActionAskCuisine(Action):
    """
    Prompt user for cuisine with the top cuisines in the user provided location

    Required Parameters: Location
    """
    def name(self) -> Text:
        return "action_ask_cuisine"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print()
        print("====Inside ActionAskCuisine====")
        print()
        # print("tracker: ",)
        channel=tracker.get_latest_input_channel()

        location=tracker.get_slot("location")
        cuisine=tracker.get_slot("cuisine")
        lat=tracker.get_slot("latitude")
        lon=tracker.get_slot("longitude")
        
        locationEntity=next(tracker.get_latest_entity_values("location"), None)
        cuisineEntity=next(tracker.get_latest_entity_values("cuisine"), None)
        user_locationEntity=next(tracker.get_latest_entity_values("user_location"), None)
        latEntity=next(tracker.get_latest_entity_values("latitude"), None)
        lonEntity=next(tracker.get_latest_entity_values("longitude"), None)

        location=tracker.get_slot("location")
        cuisine=tracker.get_slot("cuisine")
        lat=tracker.get_slot("latitude")
        lon=tracker.get_slot("longitude")
        entity_id=tracker.get_slot("location_id")
        entity_type=tracker.get_slot("location_type")
        city_id=tracker.get_slot("city_id")

       
        if(latEntity and lonEntity):
            lat=latEntity
            lon=lonEntity

        if(user_locationEntity or (latEntity and lonEntity) ):
            if(lat==None and lon==None):
                dispatcher.utter_message(text="Sure, please allow me to access your location 🧐",json_message={"payload":"location"})
                
                return []
            else:
                locationEntities=zomatoApi.getLocationDetailsbyCoordinates(lat,lon)
                location=locationEntities["title"]
                city_id=locationEntities["city_id"]
                entity_id=locationEntities["entity_id"]
                entity_type=locationEntities["entity_type"]

                SlotSet("location", locationEntities["title"])
                SlotSet("city_id", locationEntities["city_id"])
                SlotSet("location_id", locationEntities["entity_id"])
                SlotSet("location_type", locationEntities["entity_type"])


        if(locationEntity):
            locationEntities=zomatoApi.getLocationDetailsbyName(locationEntity)
            entity_id=locationEntities["entity_id"]
            entity_type=locationEntities["entity_type"]
            city_id=locationEntities["city_id"]
            SlotSet("location", locationEntities["title"])
            print("locationDetails: ",locationEntities)
            print()
        
     

        ## check if the restaurants are available in the user provided location
        if(locationEntities["restaurants_available"]=="no"):
            dispatcher.utter_message("Sorry, No restaurants available in the location you have  provided 🤯")
            return [UserUtteranceReverted()] 

        else:
            locationDetails=zomatoApi.getLocationDetails(locationEntities["entity_id"],locationEntities["entity_type"])
            if channel=="slack":
                dispatcher.utter_message(template="utter_ask_cuisine",buttons=locationDetails["top_cuisines"])
            else:
                dispatcher.utter_message(template="utter_ask_cuisine",json_message={"payload":"quickReplies","data":locationDetails["top_cuisines"]})
        
            return [SlotSet("city_id", locationEntities["city_id"]),SlotSet("location_id", locationEntities["entity_id"]),SlotSet("location_type", locationEntities["entity_type"])]


class ActionHelloWorld(FormAction):

     def name(self)->Text:
         return "feedback_form"
     
     @staticmethod
     def required_slots(tracker : Tracker) ->List[Text]:
             print("required_slots(tracker : Tracker)")
             return["name", "email","fback"]
             
     def submit(self,dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text,Any],)->List[Dict]:
         print(tracker.get_slot('fback'))
         dispatcher.utter_message(template="utter_submit",name=tracker.get_slot('name'),email=tracker.get_slot('email'),fback=tracker.get_slot('fback'))

         return []
         

def getResto_Slack(resto,show_more_results):        
    """
    prepares the restaurants details in the template format that slack requires.
    MOre details here: https://api.slack.com/tools/block-kit-builder?mode=message&blocks=%5B%7B%22type%22%3A%22section%22%2C%22text%22%3A%7B%22type%22%3A%22mrkdwn%22%2C%22text%22%3A%22We%20found%20*205%20Hotels*%20in%20New%20Orleans%2C%20LA%20from%20*12%2F14%20to%2012%2F17*%22%7D%2C%22accessory%22%3A%7B%22type%22%3A%22overflow%22%2C%22options%22%3A%5B%7B%22text%22%3A%7B%22type%22%3A%22plain_text%22%2C%22emoji%22%3Atrue%2C%22text%22%3A%22Option%20One%22%7D%2C%22value%22%3A%22value-0%22%7D%2C%7B%22text%22%3A%7B%22type%22%3A%22plain_text%22%2C%22emoji%22%3Atrue%2C%22text%22%3A%22Option%20Two%22%7D%2C%22value%22%3A%22value-1%22%7D%2C%7B%22text%22%3A%7B%22type%22%3A%22plain_text%22%2C%22emoji%22%3Atrue%2C%22text%22%3A%22Option%20Three%22%7D%2C%22value%22%3A%22value-2%22%7D%2C%7B%22text%22%3A%7B%22type%22%3A%22plain_text%22%2C%22emoji%22%3Atrue%2C%22text%22%3A%22Option%20Four%22%7D%2C%22value%22%3A%22value-3%22%7D%5D%7D%7D%2C%7B%22type%22%3A%22divider%22%7D%2C%7B%22type%22%3A%22section%22%2C%22text%22%3A%7B%22type%22%3A%22mrkdwn%22%2C%22text%22%3A%22*%3CfakeLink.toHotelPage.com%7CWindsor%20Court%20Hotel%3E*%5Cn%E2%98%85%E2%98%85%E2%98%85%E2%98%85%E2%98%85%5Cn%24340%20per%20night%5CnRated%3A%209.4%20-%20Excellent%22%7D%2C%22accessory%22%3A%7B%22type%22%3A%22image%22%2C%22image_url%22%3A%22https%3A%2F%2Fapi.slack.com%2Fimg%2Fblocks%2Fbkb_template_images%2FtripAgent_1.png%22%2C%22alt_text%22%3A%22Windsor%20Court%20Hotel%20thumbnail%22%7D%7D%2C%7B%22type%22%3A%22context%22%2C%22elements%22%3A%5B%7B%22type%22%3A%22image%22%2C%22image_url%22%3A%22https%3A%2F%2Fapi.slack.com%2Fimg%2Fblocks%2Fbkb_template_images%2FtripAgentLocationMarker.png%22%2C%22alt_text%22%3A%22Location%20Pin%20Icon%22%7D%2C%7B%22type%22%3A%22plain_text%22%2C%22emoji%22%3Atrue%2C%22text%22%3A%22Location%3A%20Central%20Business%20District%22%7D%5D%7D%2C%7B%22type%22%3A%22divider%22%7D%2C%7B%22type%22%3A%22section%22%2C%22text%22%3A%7B%22type%22%3A%22mrkdwn%22%2C%22text%22%3A%22*%3CfakeLink.toHotelPage.com%7CThe%20Ritz-Carlton%20New%20Orleans%3E*%5Cn%E2%98%85%E2%98%85%E2%98%85%E2%98%85%E2%98%85%5Cn%24340%20per%20night%5CnRated%3A%209.1%20-%20Excellent%22%7D%2C%22accessory%22%3A%7B%22type%22%3A%22image%22%2C%22image_url%22%3A%22https%3A%2F%2Fapi.slack.com%2Fimg%2Fblocks%2Fbkb_template_images%2FtripAgent_2.png%22%2C%22alt_text%22%3A%22Ritz-Carlton%20New%20Orleans%20thumbnail%22%7D%7D%2C%7B%22type%22%3A%22context%22%2C%22elements%22%3A%5B%7B%22type%22%3A%22image%22%2C%22image_url%22%3A%22https%3A%2F%2Fapi.slack.com%2Fimg%2Fblocks%2Fbkb_template_images%2FtripAgentLocationMarker.png%22%2C%22alt_text%22%3A%22Location%20Pin%20Icon%22%7D%2C%7B%22type%22%3A%22plain_text%22%2C%22emoji%22%3Atrue%2C%22text%22%3A%22Location%3A%20French%20Quarter%22%7D%5D%7D%2C%7B%22type%22%3A%22divider%22%7D%2C%7B%22type%22%3A%22section%22%2C%22text%22%3A%7B%22type%22%3A%22mrkdwn%22%2C%22text%22%3A%22*%3CfakeLink.toHotelPage.com%7COmni%20Royal%20Orleans%20Hotel%3E*%5Cn%E2%98%85%E2%98%85%E2%98%85%E2%98%85%E2%98%85%5Cn%24419%20per%20night%5CnRated%3A%208.8%20-%20Excellent%22%7D%2C%22accessory%22%3A%7B%22type%22%3A%22image%22%2C%22image_url%22%3A%22https%3A%2F%2Fapi.slack.com%2Fimg%2Fblocks%2Fbkb_template_images%2FtripAgent_3.png%22%2C%22alt_text%22%3A%22Omni%20Royal%20Orleans%20Hotel%20thumbnail%22%7D%7D%2C%7B%22type%22%3A%22context%22%2C%22elements%22%3A%5B%7B%22type%22%3A%22image%22%2C%22image_url%22%3A%22https%3A%2F%2Fapi.slack.com%2Fimg%2Fblocks%2Fbkb_template_images%2FtripAgentLocationMarker.png%22%2C%22alt_text%22%3A%22Location%20Pin%20Icon%22%7D%2C%7B%22type%22%3A%22plain_text%22%2C%22emoji%22%3Atrue%2C%22text%22%3A%22Location%3A%20French%20Quarter%22%7D%5D%7D%2C%7B%22type%22%3A%22divider%22%7D%2C%7B%22type%22%3A%22actions%22%2C%22elements%22%3A%5B%7B%22type%22%3A%22button%22%2C%22text%22%3A%7B%22type%22%3A%22plain_text%22%2C%22emoji%22%3Atrue%2C%22text%22%3A%22Next%202%20Results%22%7D%2C%22value%22%3A%22click_me_123%22%7D%5D%7D%5D

    """

    print("Show more: ",show_more_results)
    print(len(resto))
    blocks=[]
    divider={ "type": "divider" }

    blocks.append(divider)
    for i in range(0,len(resto)):
        resto_name=resto[i]["name"]
        url=resto[i]["url"]
        price=resto[i]["cost"]
        ratings=int(float(resto[i]["ratings"]))
        votes=resto[i]["votes"]
        timings=resto[i]["timings"]
        image=resto[i]["image"]
        location=resto[i]["location"]
        currency=resto[i]["currency"]
        title="<"+url+"|"+resto_name+">"
        image_url=image.replace("?output-format=webp","")
        
        stars=""
        for j in range(ratings):
            stars = stars + "★"
        text="*"+title+"*\n"+stars+"\n"+currency+str(price)+"\nRated: "+resto[i]["ratings"]+" - "+resto[i]["user_rating_text"]+"\t:+1:"+votes

        temp={ "type": "section", "text": { "type": "mrkdwn", "text": text}, "accessory": { "type": "image", "image_url": image_url, "alt_text": resto_name } }
        location_detail={ "type": "context", "elements": [{ "type": "image", "image_url": "https://api.slack.com/img/blocks/bkb_template_images/tripAgentLocationMarker.png", "alt_text": "Location Pin Icon" }, { "type": "plain_text", "text": location } ] }
        
        
        blocks.append(temp)
        blocks.append(location_detail)
        blocks.append(divider)

    if show_more_results==True:
        show_more={ "type": "actions", "elements": [ { "type": "button", "text": { "type": "plain_text", "text": "Show More" }, "value": "/show_more" } ] }
        blocks.append(show_more)

    
    return ({ "blocks": blocks })