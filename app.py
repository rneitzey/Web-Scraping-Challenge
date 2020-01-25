# import libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Set up connection inline 
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# # Connect to a database. Will create one if not already available.
# db = client.team_db

# # Drops collection if available to remove duplicates
# db.team.drop()

@app.route("/")
def home():

    mars_db = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars_db)


@app.route("/scrape")
def scraper():
    # Run the scrape function
    mars_info = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update({}, mars_info, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)