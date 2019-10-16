import os
from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
 
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
    Navigate to the list of user guitars
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
    guitars=mongo.db.guitars
    guitars.insert_one(request.form.to_dict())
    return render_template("guitars.html")


@app.route("/poll")
def poll():
    """
    Navigate to Poll page to vote on exciting guitar
    """
    mongo.db.poll_results
    return render_template("poll.html", poll_results=mongo.db.poll_results)

@app.route("/submit_vote")
def submit_vote():
    """
    Add vote results to poll results in DB
    """
    vote=request.form("vote")

if __name__ == "__main__":
    app.run(host=os.getenv("IP"), port=(os.getenv("PORT")), debug=True)