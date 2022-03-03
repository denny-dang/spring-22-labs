from crypt import methods
import sqlite3
from flask import Flask, request, Response
import uuid
import json

app = Flask(__name__)

def getDataFromFile():
    file = open('locations.json')
    data = json.load(file)
    locationMap = data['userLocation']
    file.close()
    return locationMap

def getResult(userLocations, name, location):
    if name is not None and location is not None:
        result = {key: value for key, value in userLocations.items() if key == name and value == location}
    elif name is not None:
        result = {key: value for key, value in userLocations.items() if key == name}
    elif location is not None:
        result = {key: value for key, value in userLocations.items() if value == location}
    else:
        return {
            "error": "Invalid Request - No name and location"
        }, 404
    return result, 200

@app.route("/arg", methods = ['GET'])
def getWithArgs():
    name, location = request.args.get('name'), request.args.get('location')
    userLocations = getDataFromFile()
    return getResult(userLocations, name, location)

@app.route("/form", methods = ['GET'])
def getWithForm():
    name, location = request.form.get('name'), request.form.get('location')
    userLocations = getDataFromFile()
    return getResult(userLocations, name, location)

@app.route("/file", methods = ['GET'])
def getWithFile():
    locationsFile = request.files.get('locationFile')
    fileExtension = locationsFile.filename.split('.')[1]
    if fileExtension != "json":
        return {
            "error": "Invalid File Type"
        }, 404
    if locationsFile is None:
        return {
            "error": "No locations file provided"
        }, 404
    data = json.load(locationsFile)
    userLocations = data['userLocation']
    name, location = request.form.get('name'), request.form.get('location')
    return getResult(userLocations, name, location)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)