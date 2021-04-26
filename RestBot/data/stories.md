## story_0
* chitchat
  - respond_chitchat

## story_1 search best restaurants nearby
* searchBestRestaurants{"user_location":"near by"}
  - action_search_best_restaurants
* inform{"latitude":"18.940170288085938","longitude":"72.8348617553711"}
  - utter_thanksforLocation
  - action_search_best_restaurants


## story_1_1 search best restaurants nearby(chitchat)
* searchBestRestaurants{"user_location":"near by"}
  - action_search_best_restaurants
* chitchat
  - respond_chitchat
  - action_search_best_restaurants
* inform{"latitude":"18.940170288085938","longitude":"72.8348617553711"}
  - utter_thanksforLocation
  - action_search_best_restaurants

  
## story_2 user has provided nearby location and cuisine
* searchRestaurant{"cuisine":"chinese","user_location":"near by"}
  - action_search_restaurants

  
## story_3 user has not provided any details

* searchRestaurant
    - utter_ask_location
* inform{"location":"hinjewadi"}
    - slot{"location":"hinjewadi"}
    - action_ask_cuisine
    - slot{"city_id":5}
    - slot{"location_id":3305}
    - slot{"location_type":"subzone"}
* inform{"cuisine":"chinese"}
    - slot{"cuisine":"chinese"}
    - action_search_restaurants
   
    
## story_3_1 user has not provided any details(with chitchat)

* searchRestaurant
    - utter_ask_location
* chitchat
  - respond_chitchat
  - utter_assist_location
* inform{"location":"hinjewadi"}
    - slot{"location":"hinjewadi"}
    - action_ask_cuisine
    - slot{"city_id":5}
    - slot{"location_id":3305}
    - slot{"location_type":"subzone"}
* inform{"cuisine":"chinese"}
    - slot{"cuisine":"chinese"}
    - action_search_restaurants
     

## story_4 user wants to search best restaurants but didn't provided the location

* searchBestRestaurants
    - utter_ask_location
* inform{"location":"wakad"}
    - slot{"location":"wakad"}
    - action_search_best_restaurants
   
## story_4_1 user wants to search best restaurants but didn't provided the location(with chitchat)

* searchBestRestaurants
    - utter_ask_location
* chitchat
    - respond_chitchat
    - utter_assist_location
* inform{"location":"wakad"}
    - slot{"location":"wakad"}
    - action_search_best_restaurants
        
## story_5 search restaurants details provided but bot wants to know user location

* searchRestaurant{"cuisine":"indian","user_location":"nearby"}
    - slot{"cuisine":"indian"}
    - action_search_restaurants
* inform{"latitude":18.9401702881,"longitude":72.8348617554}
    - slot{"latitude":18.9401702881}
    - slot{"longitude":72.8348617554}
    - utter_thanksforLocation
    - action_search_restaurants
    
   
## story_5_1 search restaurants details provided but bot wants to know user location, user doesn't knows the location

* searchRestaurant{"cuisine":"indian","user_location":"nearby"}
    - slot{"cuisine":"indian"}
    - action_search_restaurants
* locationUnknown
    - utter_locationUnknown
* inform{"latitude":18.9401702881,"longitude":72.8348617554}
    - slot{"latitude":18.9401702881}
    - slot{"longitude":72.8348617554}
    - utter_thanksforLocation
    - action_search_restaurants
    
   
## story_5_1_2 search restaurants details provided but bot wants to know user location, user doesn't knows the location(chitchat)

* searchRestaurant{"cuisine":"indian","user_location":"nearby"}
    - slot{"cuisine":"indian"}
    - action_search_restaurants
* chitchat
    - respond_chitchat
    - action_search_restaurants
* locationUnknown
    - utter_locationUnknown
* inform{"latitude":18.9401702881,"longitude":72.8348617554}
    - slot{"latitude":18.9401702881}
    - slot{"longitude":72.8348617554}
    - utter_thanksforLocation
    - action_search_restaurants
    
   
## story_6 search restaurants,only location provided

* searchRestaurant{"location":"lucknow"}
    - slot{"location":"lucknow"}
    - action_ask_cuisine
    - slot{"city_id":8}
    - slot{"location_id":8}
    - slot{"location_type":"city"}
* inform{"cuisine":"italian"}
    - slot{"cuisine":"italian"}
    - action_search_restaurants
    
   
## story_6_1 search restaurants,only location provided(chitchat)

* searchRestaurant{"location":"lucknow"}
    - action_ask_cuisine
* chitchat
    - respond_chitchat
    - action_ask_cuisine
* inform{"cuisine":"italian"}
    - slot{"cuisine":"italian"}
    - action_search_restaurants
    
   
## story_7 search restaurants,only cuisine provided

* searchRestaurant{"cuisine":"maharashtrian"}
    - slot{"cuisine":"maharashtrian"}
    - utter_ask_location
* inform{"location":"jaipur"}
    - slot{"location":"jaipur"}
    - action_search_restaurants
    
   
## story_7_1 search restaurants,only cuisine provided(chitchat)

* searchRestaurant{"cuisine":"maharashtrian"}
    - slot{"cuisine":"maharashtrian"}
    - utter_ask_location
* chitchat
    - respond_chitchat
    - utter_assist_location
* inform{"location":"jaipur"}
    - slot{"location":"jaipur"}
    - action_search_restaurants
    
   
## story_8_1 search restaurants and user is fine with any cuisine

* searchRestaurant{"location":"pune"}
    - slot{"location":"pune"}
    - action_ask_cuisine
    - slot{"city_id":5}
    - slot{"location_id":5}
    - slot{"location_type":"city"}
* inform
    - action_search_restaurants_without_cuisine
    
   
## story_8_2 search restaurants nearby and user is fine with any cuisine

* searchRestaurant{"user_location":"nearby"}
    - action_ask_cuisine
* inform{"latitude":18.9401702881,"longitude":72.8348617554}
    - slot{"latitude":18.9401702881}
    - slot{"longitude":72.8348617554}
    - utter_thanksforLocation
    - action_ask_cuisine
    - slot{"city_id":3}
    - slot{"location_id":2016}
    - slot{"location_type":"subzone"}

## story_9_1 user has provided the location but wants to change the location later

* searchRestaurant
    - utter_ask_location
* inform{"location":"hijnewadi"}
    - slot{"location":"hijnewadi"}
    - action_ask_cuisine
    - slot{"city_id":5}
    - slot{"location_id":3305}
    - slot{"location_type":"subzone"}
* changeLocation{"location":"wakad"}
    - slot{"location":"wakad"}
    - utter_location_change
    - action_ask_cuisine
    - slot{"city_id":5}
    - slot{"location_id":3419}
    - slot{"location_type":"subzone"}
* inform{"cuisine":"italian"}
    - slot{"cuisine":"italian"}
    - action_search_restaurants

## story_9_2 user has provided cuisine but wants to change the cuisine later

* searchRestaurant{"cuisine":"chinese"}
    - slot{"cuisine":"chinese"}
    - utter_ask_location
* changeCuisine{"cuisine":"italian"}
    - slot{"cuisine":"italian"}
    - utter_cuisine_change
    - slot{"cuisine":"chinese"}
    - slot{"cuisine":"italian"}
    - utter_ask_location
* inform{"location":"pune"}
    - slot{"location":"pune"}
    - action_search_restaurants

## story_9_3 user has provided cuisine but wants to change the cuisine later and location provided as nearby

* searchRestaurant{"cuisine":"indian"}
    - slot{"cuisine":"indian"}
    - utter_ask_location
* changeCuisine{"cuisine":"chinese"}
    - slot{"cuisine":"chinese"}
    - utter_cuisine_change
    - utter_ask_location
* inform{"user_location":"nearby"}
    - action_search_restaurants
* inform{"latitude":18.9401702881,"longitude":72.8348617554}
    - slot{"latitude":18.9401702881}
    - slot{"longitude":72.8348617554}
    - utter_thanksforLocation
    - action_search_restaurants

## story_9_4 user has provided location but wants to change the location later and location provided as nearby

* searchRestaurant{"location":"pune"}
    - slot{"location":"pune"}
    - action_ask_cuisine
    - slot{"city_id":5}
    - slot{"location_id":5}
    - slot{"location_type":"city"}
* changeLocation{"user_location":"nearby"}
    - action_ask_cuisine
* inform{"latitude":18.9401702881,"longitude":72.8348617554}
    - slot{"latitude":18.9401702881}
    - slot{"longitude":72.8348617554}
    - utter_thanksforLocation
    - utter_location_change
    - action_ask_cuisine
    - slot{"city_id":3}
    - slot{"location_id":2016}
    - slot{"location_type":"subzone"}
* inform{"cuisine":"chinese"}
    - slot{"cuisine":"chinese"}
    - action_search_restaurants
    
## story_10 restaurants not available in user provided location
* inform{"cuisine":"indian","location":"karjat"}
    - slot{"cuisine":"indian"}
    - slot{"location":"karjat"}
    - action_search_restaurants
* changeLocation{"location":"neral"}
    - slot{"location":"neral"}
    - utter_location_change
    - action_search_restaurants
    
   
## story_11 user has not provided any details and doesn't know location

* searchRestaurant
    - utter_ask_location
* locationUnknown
    - utter_locationUnknown
* inform{"latitude":18.9401702881,"longitude":72.8348617554}
    - slot{"latitude":18.9401702881}
    - slot{"longitude":72.8348617554}
    - utter_thanksforLocation
    - action_ask_cuisine
* inform{"cuisine":"chinese"}
    - slot{"cuisine":"chinese"}
    - action_search_restaurants
    
   
## story_12 user has not provided any details and provided his current location

* searchRestaurant
    - utter_ask_location
* inform{"user_location":"near by"}
    - action_ask_cuisine
* inform{"latitude":18.9401702881,"longitude":72.8348617554}
    - slot{"latitude":18.9401702881}
    - slot{"longitude":72.8348617554}
    - utter_thanksforLocation
    - action_ask_cuisine
* inform{"cuisine":"chinese"}
    - slot{"cuisine":"chinese"}
    - action_search_restaurants
    
   
## story_13 user has not provided any details and denys to provide access to his current location

* searchRestaurant
    - utter_ask_location
* inform{"user_location":"near by"}
    - action_ask_cuisine
* inform{"user_location":"deny"}
    - utter_location_denied
    
   
## story_14 show more restaurants
* searchRestaurant{"cuisine":"chinese","location":"berlin"}
    - action_search_restaurants
* show_more
    - action_show_more_results
    
   
## story_15 show more restaurants
* searchRestaurant
    - utter_ask_location
* inform{"location":"hinjewadi"}
    - slot{"location":"hinjewadi"}
    - action_ask_cuisine
    - slot{"city_id":5}
    - slot{"location_id":3305}
    - slot{"location_type":"subzone"}
* inform{"cuisine":"chinese"}
    - slot{"cuisine":"chinese"}
    - action_search_restaurants
* show_more
    - action_show_more_results
      
## feedback path
*feedback
  -utter_feedback
  -feedback_form
  -form{"name": "feedback_form"}
  -form{"name": null}
  -utter_slots_values
  -utter_ask_feedback
*thankyou
  -utter_goodbye