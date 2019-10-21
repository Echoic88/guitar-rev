import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
 
app = Flask(__name__)
app.config["MONGODB_NAME"] = "guitarReview"
app.config["MONGO_URI"] = os.getenv("mongoURI")
app.secret_key = os.getenv("sessionKey")
mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    """ 
    Navigate to home page
    """
    try:
        user = mongo.db.users.find_one({"user_name":request.form.get("user_name")})
        return render_template("index.html", user=user)
    except:
        return render_template("index.html", user=user)


@app.route("/get_user", methods=["GET", "POST"])
def get_user():
    """
    Retrieve user details
    """
    user = mongo.db.users.find_one({"user_name":request.form.get("user_name")})
    
    try:       
        #Add user id to session cookie to navigate between pages
        session["user_id"] = str(user["_id"])
        return render_template("index.html", user=user)

    except:
        print("NO SUCH USER")
        return redirect("/index")


@app.route("/edit_user", methods=["GET", "POST"])
def edit_user():
    try:
        user = mongo.db.users.find_one({"_id":ObjectId(session["user_id"])})
        return render_template("edit-user.html", user=user)
    except:
        print("No user logged in")
        return redirect("/index")



@app.route("/update_user", methods=["POST"])
def update_user():
    """
    Update user details in DB
    """
    mongo.db.users.update_one({"_id":ObjectId(session["user_id"])}, {"$set": 
                                                        {"first_name":request.form.get("first_name"),
                                                        "surname":request.form.get("surname")}})
    return render_template("index.html")


@app.route("/delete_user")
def delete_user():
    """
    Delete the current user
    """
    mongo.db.users.remove({"_id":ObjectId(session["user_id"])})
    return redirect("index.html")


@app.route("/guitars")
def guitars():
    """
    Navigate to guitars.html
    """
    user = users.find_one({"_id":ObjectId(session["user_id"])})
    guitars = mongo.db.guitars

    return render_template("guitars.html", guitars=guitars.find(), user=user)


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
    DB entry in guitars and users collections
    """
    user = users.find_one({"_id":ObjectId(session["user_id"])})
    guitars = mongo.db.guitars 
    
    try:
        #Insert the guitar data from the form into guitars collection
        #return the newly created guitar object id to variable gtr_id
        guitars.insert_one({
            "gtr_name":request.form.get("gtr_name"),
            "brand":request.form.get("brand"),
            "gtr_type":request.form.get("gtr_type"),
            "pickup_config":request.form.get("pickup_config"),
            "rating":request.form.get("rating"),
            "comment":request.form.get("comment"),
            "user_id":user
        })
        return render_template("guitars.html")
    except:
        print("NO SUCH USER")
        return redirect("/index")
    

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


if __name__ == "__main__":
    app.run(host=os.getenv("IP"), port=(os.getenv("PORT")), debug=True)