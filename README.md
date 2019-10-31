# Guitar Review

A basic website that allows users to submit reviews of their guitars and to vote in a user poll for the guitar they are most excited about this year. To submit a review of their own guitar users are required to log in. Emulating polls on other webistes, no user login is required to submit a vote in the poll or to view the results.

***

## UX

No wireframe used for this project.

* Navbar

  * The title of the page "Guitar Review" provides a link back to the home page on all pages.

  The navbar links to three primary pages.

  * Home - where an existing user can log in. No password is currently required. The user can also register their details (First name and last name only required) from this page.
  * Your Guitars - Where a user can submit a review of guitars that they own and view reviews of existing reviews. Access to this page Requires a user to be logged in. Users can select to edit or delete their profile from this page.
  * Poll - Where a user can vote in a website poll for "Guitars they are most excited asbout in 2019". There is also the option to view the current results os the poll. No login is required to access this page.

***

## Features

* Users can review guitars that they own entering values for
  * Guitar name
  * Brand
  * Guitar Type
  * User rating (Between 0 and 5)
  * Upload image if the guitar (from local storage)

* Users can edit and delete their personal details from the website.

* Users can participate in a poll and view the results along with a basic chart displaying the results.

***

## Features left to implement

* Add password to user login.
* Ability for users to edit and delete existing reviews.
* Add user confirmation before deleting a user.
* Add option to remove user revies when a user is deleted.
* Make guitar image upload optional and provide a placeholder image for relevant guitar details if no image has been provided by the user.
* Improved UI across all pages.

***

## Technologies Used

* Materialize - used primarily for grid layout of pages.
Also used for collapsible Navbar and buttons across pages
https://materializecss.com/
* Jquery - Used to support Materialize.
https://jquery.com/
* Python - Used for handling data to and from mongoDB and routing between the pages.
https://www.python.org/
* DC/Crossfilter/D3 - Used for chart displaying poll results.
https://square.github.io/crossfilter/  
https://d3js.org/  
https://github.com/dc-js/dc.js/wiki
* Mongo DB - Provides database backend where user, guitar and poll details are saved.
https://cloud.mongodb.com/user?signedOut=true#/atlas/login
* Cloudinary - Hosts images for the site.
https://cloudinary.com/
* Heroku - Used for live deployment of the website.
https://www.heroku.com/

***

## Testing

Two test users are provided with existing personal details and guitar reviews:

* Aaron55
* Brandy75

Tested on

* Windows Chrome
* Windows Firefox
* Android Chrome
* Android Firefox

***

## Bugs/Issues

* When user is logged in and returns to the Home page the user greeting "Hi username" is not displayed"
* Edit User Details page: on submitting user details the updated details are not returned to the user onscreen until the page is refreshed.
* Ensure proper responsiveness of buttons on Home page.

***

## Deployment

* Create requirements.txt to provide Heroku with Python package requirements.  
Packages required are:
certifi==2019.9.11  
Click==7.0  
cloudinary==1.18.2  
dnspython==1.16.0  
Flask==1.1.1  
Flask-PyMongo==2.3.0  
itsdangerous==1.1.0  
Jinja2==2.10.3  
MarkupSafe==1.1.1  
mock==3.0.5  
Pillow==6.2.1  
pymongo==3.9.0  
six==1.12.0  
urllib3==1.25.6  
Werkzeug==0.16.0

* Create Procfile to instruct Heroku to run app.py Python file on startup.
* Set Debug to False in app.py.
* Create new app in Heroku dashboard: guitar-review.
* Log into Heroku from the CLI.
* Create new Heroku remote.
* Push all files to Heroku
* In Heroku dashboard supply config variables for:  
IP - supply the IP address  
PORT - supply the port  
MONGO_URI - To connect to MongoDB  
SECRET_KEY - To provide the Flask secret key  
CLOUDINARY_URL - To connect to Cloudinary  
* From Heorku CLI launch app using ps:scale web=1

Production application link:  
https://guitar-review.herokuapp.com/

## Credits

Website inspired by Ultimate Guitar  
https://www.ultimate-guitar.com/
