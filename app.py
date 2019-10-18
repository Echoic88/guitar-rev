import os
from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import copy
 
app = Flask(__name__)
app.config["MONGODB_NAME"] = "guitarReview"
app.config["MONGO_URI"] = os.getenv("mongoURI")
mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    """ 
    Navigate to home page
    """
    return render_template("base.html")


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


@app.route("/input_guitar", methods=["POST"])
def input_guitar():
    """
    Insert details from the guitars_form to a new
    DB entry in guitars collection
    """
    guitars = mongo.db.guitars
    users = mongo.db.users
    """
    form_output = request.form.to_dict()
    guitar_data = copy.copy(form_output)
    user=guitar_data.pop("user_name")
    """
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


    #Insert a new user to users collection
    #Add the guitar name from the form and the newly created guitar id the 
    #the object containing the users guitars
    users.insert_one({
            "user_name":request.form.get("user_name"),
            "user_guitars":{request.form.get("gtr_name"):gtr_id}
    })
    
    return render_template("guitars.html")


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
    user_name = request.form.get("user_name")
    user_vote = {"ballot":user_name}
    mongo.db[vote].insert(user_vote)
    print(vote)


    return render_template("poll.html")
    

if __name__ == "__main__":
    app.run(host=os.getenv("IP"), port=(os.getenv("PORT")), debug=True)