import os
from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
 
app = Flask(__name__)
app.config["MONGODB_NAME"] = "guitarReview"
app.config["MONGO_URI"] = os.getenv("mongoURI")
mongo = PyMongo(app)


@app.route("/")
def test():
    
    return render_template("test2.html", guitars=mongo.db.guitars.find())


if __name__ == "__main__":
    app.run(host=os.getenv("IP"), port=(os.getenv("PORT")), debug=True)