from flask import Flask, jsonify, request

from collections import Counter
import spacy

from pymongo import MongoClient
from bson.objectid import ObjectId
import keyring

# Load NLP model
nlp = spacy.load('en_core_web_sm')

# Initialize MongoDB connection
dbName = "pai0"
dbUser = "testuser"
pwd = keyring.get_password(dbName, dbUser)
connectStr = "mongodb+srv://{}:{}@cluster0.kad14.mongodb.net/{}?retryWrites=true&w=majority".format(
    dbUser, pwd, dbName
)

client = MongoClient(connectStr)
db = client.get_database(dbName)
db_wordfreq = db.get_collection("wordfreq")

# Setup Flask with the REST endpoints
app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello, Flask!</p>"


@app.route("/rest", methods=["GET"])
def get_rest():
    restDescription = [
        {
            "route": "/rest",
            "methods": ["GET"],
            "description": "This route: The API documentation",
        },
        {
            "route": "/rest/texts",
            "methods": ["GET"],
            "description": "List available text IDs along with their first phrase",
        },
        {
            "route": "/rest/texts",
            "methods": ["POST"],
            "description": "Adds a new text. \n \
                If the request header is 'application/json', only the 'text' property is parsed. \n  \
                Otherwise, the full request body is parsed as a string, assuming utf8 encoding.",
        },
        {
            "route": "/rest/texts/<id>",
            "methods": ["GET"],
            "description": "Gets the text matching the ID",
        },
        {
            "route": "/rest/texts/<id>",
            "methods": ["DELETE"],
            "description": "Removes the text matching the ID",
        },
        {
            "route": "/rest/texts/<id>/freq",
            "methods": ["GET"],
            "description": "Get word frequency for text matching ID",
        },
    ]
    return jsonify(restDescription)


@app.route("/rest/texts", methods=["GET"])
def get_all_texts():
    project = {"$project": {"_id": {"$toString": "$_id"}, "intro": 1}}
    pipeline = [project]
    cursor = db_wordfreq.aggregate(pipeline)
    texts = list(cursor)
    return jsonify(texts)


@app.route("/rest/texts", methods=["POST"])
def add_text():

    # Parse text from the request
    if request.is_json:
        req_json = request.json
        text = req_json["text"]
    else:
        data = request.data
        text = data.decode('utf8')
    
    # Extract the first sentence, count the frequencies
    doc = nlp(text)
    intro = next(doc.sents).text
    counter = Counter()
    for token in doc:
        if not token.is_stop:
            counter[token.lemma_] += 1
    obj = {
    'text': text,
    'intro': intro,
    'freq': counter
    }

    # Push to the database and return th text id
    ins = db_wordfreq.insert_one(obj)
    id = str(ins.inserted_id)
    return jsonify({'_id': id})


@app.route("/rest/texts/<id>", methods=["GET"])
def get_text_by_id(id):
    # Should add some checks on the ID
    try:
        fltr = {"$match": {"_id": ObjectId(id)}}
        project = {"$project": {"_id": 0, "text": 1}}
        pipeline = [fltr, project]
        cursor = db_wordfreq.aggregate(pipeline)
        text = list(cursor)[0]
        return jsonify(text)
    except:
        # I get a bson.errors.InvalidId if I cannot convert the string to ObjectID
        print('Something went wrong')
        pass


@app.route("/rest/texts/<id>/freq", methods=["GET"])
def get_freq_by_id(id):
    # Should add some checks on the ID
    try:
        fltr = {"$match": {"_id": ObjectId(id)}}
        project = {"$project": {"_id": 0, "freq": 1}}
        pipeline = [fltr, project]
        cursor = db_wordfreq.aggregate(pipeline)
        text = list(cursor)[0]
        return jsonify(text)
    except:
        # I get a bson.errors.InvalidId if I cannot convert the string to ObjectID
        print('Something went wrong')
        pass

if __name__ == "__main__":
    app.run(debug=True)
