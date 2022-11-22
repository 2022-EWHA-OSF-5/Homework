from flask import Flask, render_template, request, redirect,url_for
from database import DBhandler
import sys

application = Flask(__name__)
DB = DBhandler()

@application.route("/") 
def home():
    return redirect(url_for('list_restaurants'))

@application.route("/list") #리스트
def list_restaurants():
    page = request.args.get("page", 0, type=int)
    limit = 10
    start_idx=limit*page
    end_idx=limit*(page+1)
    data = DB.get_restaurants() #read the table
    tot_count = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    print('뿌려짐', data)
    return render_template(
        "list.html",
        datas=data.items(),
        total=tot_count,
        limit=limit,
        page=page,
        page_count=int((tot_count/10)+1))

@application.route('/dynamicurl/<varible_name>/') #다이내믹
def DynamicUrl(varible_name):
    return str(varible_name)

@application.route("/view_detail/<name>/") #디테일
def view_restaurant_detail(name):
    data = DB.get_restaurant_byname(str(name))
    avg_rate = DB.get_avgrate_byname(str(name))
    return render_template("detail.html", data=data, avg_rate=avg_rate)

@application.route("/list_foods/<res_name>/") # 식당 이름 기반 동적 라우팅
def view_foods(res_name):
    data = DB.get_food_byname(str(res_name))
    tot_count = len(data)
    page_count = len(data)
    return render_template(
        "food_list.html",
        datas=data,
        total=tot_count)

@application.route("/list_reviews/<res_name>/") # 특정 식당의 리뷰 보기 
def view_reviews(res_name):
    data = DB.get_review_byname(str(res_name))
    print('뿡뿡', data)
    tot_count = len(data)
    print('토탈', tot_count)
    return render_template(
        "review_list.html",
        datas=data,
        total=tot_count)
    #get_avgrate_byname 평균 별점?? 

@application.route("/register_restaurant") 
def register_restaurant():
    return render_template("register_restaurant.html")

@application.route("/register_menu") 
def register_menu():
    return render_template("register_menu.html")

@application.route("/register_menu", methods=['POST']) 
def reg_menu():
    data=request.form 
    return render_template("register_menu.html", data=data)

@application.route("/register_review") 
def register_review():
    return render_template("register_review.html")

@application.route("/register_review", methods=['POST']) 
def reg_review():
    data=request.form 
    return render_template("register_review.html", data=data)



@application.route("/submit_restaurant_post", methods=['POST']) 
def submit_restaurant_post():
    if request.files["file"] :
        image_file=request.files["file"] 
        image_path = "static/image/{}".format(image_file.filename)
        image_file.save(image_path) 
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
    else:
        image_path=""
    data=request.form
    DB.insert_menu(data['menu_name'], data, image_path)

    return render_template("index.html", data=data)


@application.route("/submit_review_post", methods=['POST']) 
def submit_review_post():
    data=request.form
    DB.insert_review(data['res_name'], data)

    return render_template("index.html", data=data)

if __name__ == "__main__": application.run(host='0.0.0.0')