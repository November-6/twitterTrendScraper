from flask import Flask, render_template, jsonify
import scrape
from flask_pymongo import PyMongo 
from pymongo import MongoClient


app = Flask(__name__)

app.config["MONGO_URI"] = 'mongodb+srv://nayaa3231:bWmgxZgpyEHaxFYA@internproject.flgvh.mongodb.net/'
client = MongoClient(app.config["MONGO_URI"])
db = client.flask_database
collection = db.collection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['GET', 'POST'])
def run_script():
    data = scrape.scrape_twitter()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port = 5001)
