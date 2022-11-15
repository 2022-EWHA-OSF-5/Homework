import pyrebase
import json

class DBhandler:
    def __init__(self ):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f )

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    def restaurant_duplicate_check(self, name): 
        restaurants = self.db.child("restaurant").get() 
        for res in restaurants.each():
            if res.key() == name: 
                return False
            return True
    
    def insert_restaurant(self, name, data, path):
        restaurant_info ={
            "location": data['location'],
            "addr": data['addr'],
            "tel": data['tel'],
            "category": data['category'],
            "park": data['park'],
            "site": data['website'],
            "time": data['time'],
            "price": data['price'],
            "reserve": data['reserve'],
            "img": path,
        }
        if self.restaurant_duplicate_check(name): 
            self.db.child("restaurant").child(name).set(restaurant_info) 
            print(data, path)
            return True
        else:
            return False
    