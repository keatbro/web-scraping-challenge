from flask import Flask, render_template, Response, request, redirect, url_for
import scrape_mars
import pymongo

# Configure Flask app
app = Flask(__name__)

# Connect to MongoDB
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Create database
db = client.mars_db

# Set routes for app
@app.route('/')
def index():
    data = db.data_table.find() 
    return render_template("index.html", dataDict = data)

@app.route('/scrapenewdata')
def scrape():

    # Delete old data
    db.data_table.drop()

    data = scrape_mars.scrape()
    db.data_table.insert_one(data)
    return redirect("/")

if __name__ == '__main__':
   app.run()