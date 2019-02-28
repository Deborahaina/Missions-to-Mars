from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


# Use flask_pymongo to set up mongo connection locally 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 

    # Find data
    mars = mongo.db.mars_data.find_one()
    table= mongo.db.mars_table.find_one()
    # Return template and data
    return render_template("index.html", mars=mars, table=table)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape():
    
    mars_data = mongo.db.mars_data
    mars_d = scrape_mars.scrape()
    mars_data.update({}, mars_d, upsert=True)
    return redirect("/", code=302)


@app.route('/shutdown')
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Shutting down Flask server...'


if __name__ == "__main__":
    app.run(debug=True)