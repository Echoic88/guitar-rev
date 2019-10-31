import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import json
import random
import cloudinary
import cloudinary.utils
import cloudinary.uploader

app = Flask(__name__)
app.config["MONGODB_NAME"] = "guitarReview"
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


cloudinary.config.update = ({
    'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
})

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    """
    Navigate to home page
    """

    try:
        user = mongo.db.users.find_one({"user_name": request.form.get("user_name")})
        return render_template("index.html", user=user, page_title="Home")
    except:
        session["user_id"] = str("")
        return render_template("index.html", page_title="Home")


@app.route("/register")
def register():
    """
    Navigate to registration form for new users
    """
    return render_template("register.html", page_title="Register")


@app.route("/register_user", methods=["POST"])
def register_user():
    """
    Create new user from register user form
    """
    if request.method == "POST":
        name = request.form.get("first_name")
        mongo.db.users.insert_one(request.form.to_dict())
        flash("You are now registered")
        return render_template("register.html", page_title="Register")


@app.route("/get_user", methods=["POST"])
def get_user():
    """
    Retrieve user details and route to guitars page
    """
    
    # Add user id to session cookie to navigate between pages
    try:
        user = mongo.db.users.find_one({"user_name": request.form.get("user_name")})
        session["user_id"] = str(user["_id"])
        return redirect("/guitars")

    except:
        flash("Sorry. Thats user isnt recognised")
        return redirect("/index")


@app.route("/logout")
def logout():
    """
    Logout User
    """
    session["user_id"] = ""
    flash("You are now logged out")
    return redirect("/index")


@app.route("/edit_user", methods=["GET", "POST"])
def edit_user():
    try:
        user = mongo.db.users.find_one({"_id": ObjectId(session["user_id"])})
        return render_template("edit-user.html", user=user)
    except:
        print("No user logged in")
        return redirect("/index")


@app.route("/update_user", methods=["POST"])
def update_user():
    """
    Update user details in DB
    """
    if request.method == "POST":
        user = mongo.db.users.find_one({"_id": ObjectId(session["user_id"])})
        mongo.db.users.update_one({"_id": ObjectId(session["user_id"])}, {"$set":
                                                            {"first_name": request.form.get("first_name"),
                                                            "surname": request.form.get("surname")}})
        flash("Details updated")
        return render_template("edit-user.html", user=user, page_title="Edit Details")


@app.route("/delete_user")
def delete_user():
    """
    Delete the current user
    """
    try:
        user = mongo.db.users.find_one({"_id": ObjectId(session["user_id"])})
        mongo.db.users.delete_one({"_id": ObjectId(session["user_id"])})
        flash("Sorry to see you go {}")
        return redirect("/index")

    except:
        print("Delete User Failed")
        return redirect("/index")  
    

@app.route("/guitars")
def guitars():
    """
    Navigate to guitars.html
    """

    try:
        user = mongo.db.users.find_one({"_id": ObjectId(session["user_id"])})
        guitars = mongo.db.guitars.find({"user_id": ObjectId(session["user_id"])})
        return render_template("guitars.html", guitars=guitars, user=user, page_title="Your Guitars")

    except:
        # if no user then return to home page
        print("Fail to retrive guitars/guitars page")
        return redirect("/index")


@app.route("/guitars_form")
def guitars_form():
    """
    When "Tell Us About Your Guitar" button is
    pressed navigate to guitars form
    """
    user = mongo.db.users.find_one({"_id": ObjectId(session["user_id"])})
    return render_template("guitars-form.html", user=user, page_title="New Guitar")


@app.route("/input_guitar", methods=["POST"])
def input_guitar():
    """
    Insert details from the guitars_form to a new
    DB entry in guitars collections
    """
    user = mongo.db.users.find_one({"_id": ObjectId(session["user_id"])})
    guitars = mongo.db.guitars

    if request.method == 'POST':
        img = request.files["image_id"]
        # the image id will be the ObjectID for the
        # user in Mongo DB concatenated with a random number
        img_id = str(session["user_id"])+"-"+str(random.randint(1, 9999999))

    cloudinary.uploader.upload(
        img, public_id=img_id
    )

    img_url = cloudinary.utils.cloudinary_url(img_id)

    # Insert the guitar data from the
    # form and user id into guitars collection
    guitars.insert_one({
        "gtr_name": request.form.get("gtr_name"),
        "brand": request.form.get("brand"),
        "gtr_type": request.form.get("gtr_type"),
        "rating": int(request.form.get("rating")),
        "comment": request.form.get("comment"),
        "image_id": img_url[0],
        "user_id": ObjectId(session["user_id"])
    })

    return redirect("/guitars")


@app.route("/poll")
def poll():
    """
    Navigate to poll.html
    """
    return render_template("poll.html", page_title="2019 Poll")


@app.route("/submit_vote", methods=["POST"])
def submit_vote():
    """
    Add vote results to individual collections in DB for results
    """
    vote = request.form.get("vote")
    mongo.db.total_votes.insert_one({"vote": vote})
    flash("Thanks for voting")
    return render_template("poll.html", page_title="2019 Poll")


@app.route("/poll_results")
def poll_results():
    """
    Display poll results when Vew Results button is pressed
    """
    results = mongo.db.total_votes
    get_votes = [{"$group": {"_id": "$vote", "number_of_votes": {"$sum": 1}}}]
    votes_per_guitar = list(results.aggregate(get_votes))

    # get individual results
    votes_dict = {}
    for i in range(len(votes_per_guitar)):
        votes_dict[votes_per_guitar[i]["_id"]] = votes_per_guitar[i]["number_of_votes"]

    return render_template("poll-results.html", results=votes_dict, resList=json.dumps(votes_per_guitar), page_title="Poll Results")

if __name__ == "__main__":
    app.run(host=os.getenv("IP"), port=(os.getenv("PORT")), debug=False)
