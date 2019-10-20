import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import copy
 
app = Flask(__name__)
app.config["MONGODB_NAME"] = "guitarReview"
app.config["MONGO_URI"] = os.getenv("mongoURI")
mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    """ 
    Navigate to home page
    """
    return render_template("index.html")


@app.route("/guitars")
def guitars():
    """
    Navigate to guitars.html
    """
    guitars = mongo.db.guitars
    return render_template("guitars.html", guitars=guitars.find())


@app.route("/guitars_form")
def guitars_form():
    """
    When "Tell Us About Your Guitar" button is
    pressed navigate to guitars form 
    """
    return render_template("guitars-form.html")


"""
@app.route("/input_guitar", methods=["POST"])
def input_guitar():
    
    #Insert details from the guitars_form to a new
    #DB entry in guitars and users collections
    
    guitars = mongo.db.guitars
    users = mongo.db.users

    
    this_user=users.find_one({"user_name":request.form.get("user_name")})
    


    #Insert the guitar data from the form into guitars collection
    #return the newly created guitar object id to variable gtr_id
    gtr_id = guitars.insert_one({
            "gtr_name":request.form.get("gtr_name"),
            "brand":request.form.get("brand"),
            "gtr_type":request.form.get("gtr_type"),
            "pickup_config":request.form.get("pickup_config"),
            "rating":request.form.get("rating"),
            "comment":request.form.get("comment")
        }).inserted_id

    #Add the guitar name from the form and the newly created guitar id to 
    #the object containing the users guitars

    user_guitars = "user_guitars"
    guitars_dict= this_user.user_guitars

    users.update(this_user,
        {"$set": {guiatrs_dict:{request.form.get("gtr_name"): gtr_id}} 
        })

    return render_template("guitars.html")
"""










@app.route("/poll")
def poll():
    """
    Navigate to poll.html
    """
    return render_template("poll.html")


@app.route("/submit_vote", methods=["POST"])
def submit_vote():
    """
    Add vote results to individual collections in DB for results 
    """
    vote = request.form.get("vote")
    mongo.db[vote].insert_one({"vote":vote})
    return render_template("poll.html")


@app.route("/register")
def register():
    """
    Navigate to registration form for new users
    """
    return render_template("register.html")


@app.route("/register_user", methods=["POST"])
def register_user():
    """
    Create new user from register user form
    """
    mongo.db.users.insert_one(request.form.to_dict())
    return render_template("register.html")


@app.route("/edit_user")
def edit_user():
    """
    Navigate to page to edit/delete user details
    """
    return render_template("edit-user.html")


@app.route("/get_user_details")
def get_user_details():
    """
    Retrieve user details from db
    """
    users = mongo.db.users
    this_user=users.find_one({"user_name":request.form.get("user_name")})
    for x in this_user:
        print(x)






if __name__ == "__main__":
    app.run(host=os.getenv("IP"), port=(os.getenv("PORT")), debug=True)