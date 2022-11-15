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
    
    def insert_menu(self, name, data, path):
        menu_info = {
            "menu_name": data['menu_name'],
            "menu_price": data['menu_price'],
            "img": path,
        }
        print(menu_info)
        self.db.child("menu").child(name).set(menu_info) 
        return True

    def insert_review(self, name, data):
        review_info = {
            "star": data['star'],
            "text": data['text'],
        }
        self.db.child("review").child(name).set(review_info) 
        return True

    