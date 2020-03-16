from flask import Flask, render_template, Response, request, redirect, url_for
import scrape_mars
import pymongo

# Configure Flask app
app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['mars_db']
web_data = db['data']

@app.route('/')
def index():
    dataDict = scrape_mars.scrape()
    web_data.insert_one(dataDict)
    return render_template('index.html', data=dataDict)

@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    newMarsData = scrape_mars.scrape()
    mars_data.update({}, newMarsData, upsert=True)
    return redirect("/", code=302)


if __name__ == '__main__':
   app.run()