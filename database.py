import pyrebase
import json

class DBhandler:
    def __init__(self ):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f )

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def get_restaurants(self):
        restaurants = self.db.child("restaurant").get().val()
        return(restaurants)
    
    def restaurant_duplicate_check(self, name): 
        restaurants = self.db.child("restaurant").get()
        print(restaurants)
        if restaurants:
            for res in restaurants.each():
                value = res.val()
                if value['name'] == name: 
                    return False
                return True
    
    def insert_restaurant(self, name, data, path):
        restaurant_info ={
            "name": name,
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
           self.db.child("restaurant").push(restaurant_info)
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
            "res_name" : data['res_name'],
            "star": data['star'],
            "text": data['text'],
        }
        self.db.child("review").child(name).set(review_info) 
        return True

    def get_restaurant_byname(self, name):
        restaurants = self.db.child("restaurant").get()
        target_value=""
        for res in restaurants.each():
            value = res.val()
            if value['name'] == name:
                target_value=value
                return target_value

    def get_food_byname(self, name):
        restaurants = self.db.child("menu").get()
        target_value=[]
        for res in restaurants.each():
            value = res.val()
            if value['res_name'] == name:
                target_value.append(value)
                return target_value

    def get_avgrate_byname(self,name):
        reviews = self.db.child("review").get()
        rates=[]
        for res in reviews.each():
            value = res.val()
            print('뭐야', value)
            if value['res_name'] == name:
                rates.append(float(value['rate']))
                return sum(rates)/len(rates)