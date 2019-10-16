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
    return render_template("base.html")


@app.route("/guitars")
def guitars():
    guitars = mongo.db.guitars
    return render_template("guitars.html", guitars=guitars.find())


@app.route("/poll")
def poll():
    guitars = mongo.db.guitars
    return render_template("poll.html", guitars=guitars.find())


if __name__ == "__main__":
    app.run(host=os.getenv("IP"), port=(os.getenv("PORT")), debug=True)