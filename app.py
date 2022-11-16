from flask import Flask, render_template, request
from database import DBhandler
import sys

application = Flask(__name__)
DB = DBhandler()

@application.route("/") 
def home():
    return render_template("index.html")
@application.route("/list") 
def list():
    return render_template("list.html")
@application.route("/register_restaurant") 
def register_restaurant():
    return render_template("register_restaurant.html")
@application.route("/register_menu") 
def register_menu():
    return render_template("register_menu.html")
@application.route("/register_review") 
def register_review():
    return render_template("register_review.html")

@application.route("/register_menu", methods=['POST']) 
def reg_menu():
    data=request.form 
    print(data)
    return render_template("register_menu.html", data=data)

@application.route("/submit_restaurant_post", methods=['POST']) 
def submit_restaurant_post():
    if request.files["file"] :
        image_file=request.files["file"] 
        image_path = "static/image/{}".format(image_file.filename)
        image_file.save(image_path) 
        print(image_path)
    else:
        image_path=""
    data=request.form

    if DB.insert_restaurant(data['name'], data, image_path):
        return render_template("result.html", data=data, path=image_path)
    else:
        return "Restaurant name already exist!"


@application.route("/submit_menu_post", methods=['POST']) 
def submit_menu_post():
    if request.files["file"] :
        image_file=request.files["file"] 
        image_path = "static/image/{}".format(image_file.filename)
        image_file.save(image_path) 
        print(image_path)
    else:
        image_path=""
    data=request.form
    DB.insert_menu(data['menu_name'], data, image_path)

    return render_template("index.html", data=data)


@application.route("/submit_review_post", methods=['POST']) 
def submit_review_post():
    data=request.form
    print(data)
    DB.insert_review(data['text'], data)

    return render_template("index.html", data=data)

if __name__ == "__main__": application.run(host='0.0.0.0')