# Dependencies
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars


# create instance of Flask app
app = Flask(__name__)


# we still meed to tell the library where the database is and provde a connection string to Mongo
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Connect to the database scraped_mars. it will create it if not available
db = client.scraped_mars

#collection in the database
collection = db.mars

# Set route to query the mongo database and find all the items in the collections.Set it to a variable.
#pass the mars data into an HTML template to display the data.
@app.route('/')
def index():
    data_mars = list( collection.find() )
    print(data_mars)
    return render_template('index.html', data_mars=data_mars)


@app.route('/scrape')
def scrape():
    collection = db.mars
#import your scrape_mars.py script and call your scrape function.
    mars_data = scrape_mars.scrape()
    collection.update({},mars_data,upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
