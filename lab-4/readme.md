# Lab 4

Learning Objectives:
This lab focuses on the different methods to get data from your API request
    a. Argument - /search?name="John"
    b. Form - Getting data from an HTTP form
    c. File Uploads - Handling file uploads and reading data from it.

### Creating Common Functions
First, we create some common functions that will be used repeatedly by all of our 3 endpoints.
We will create 2 functions:
1. `getDataFromFile()` function that reads data from an external JSON file which holds the name and location of users.

```
# locations.json
{
    "userLocation": {
        "John": "Delhi",
        "Rishabh": "Berkeley",
        "Dylan": "San Francisco",
        "Mary": "New York",
        "Ben": "Berkeley"
    }
}
```

```
def getDataFromFile():
    file = open('locations.json')
    data = json.load(file)
    locationMap = data['userLocation']
    file.close()
    return locationMap
```
We use `json.load()` from the `json` module in Python to read the data from the `locations.json` file and then return the name-location mapping fetched from this file.


2. `getResult(userLocations, name, location)` function that receives the location data from the file, the name and location recieved from the API request that needs to be searched within the file data.

```
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
```
This function iterates over all items in `userLocations` dictionary/mapping. We use the [items()](https://www.w3schools.com/python/ref_dictionary_items.asp) function that returns the key, value pair in the dictionary as a list of tuples.
Based on our name and location received from the API, we either return a result or an error (in case that both name and location are not passed).
A sucessful result can be of 3 types:
    a. Both name and location are passed - We match for the record against both and return the mapping that matches or an empty response indicating that no match was found.
    b. Only name is passed - We return the first record with the name that matches the name. (_Point to ponder: Why only the first record?_)
    c. Only location is passed - We return all records that match the location.
We return an error in case both `name` and `location` are _None_.

### Getting data using URL parameters (args)

**Route: "/arg"**

We use query parameters as part of the URL to fetch the name and location that we want to search against.
When both of these parameters are passed, the endpoint would look something like `localhost:8000/arg?name=Rishabh&location=Berkeley` or when only  one of them is passed, it might look like `localhost:8000/arg?location=Berkeley`. Notice the '&' in between the two parameters. This is how we distribute multiple parameters.

```
@app.route("/arg", methods = ['GET'])
def getWithArgs():
    name, location = request.args.get('name'), request.args.get('location')
    userLocations = getDataFromFile()
    return getResult(userLocations, name, location)
```
We use `request.args` to get the arguments being passed as part of the API GET request. This will give you the data in the form of an `ImmutableMultiDict` which is a dictionary and hence you can fetch data using a key. In the code above, we could have also done `request.args['name]` but there is a reason to use `get()` function.

If we use `request.args['name]` and name is not passed as part of your arguments, this will return an error as that key (name in this case) is not present in the dictionary being returned by `request.args` but the `get()` function will assign the value of None to the variable if the key is not present. So if my endpoint is `localhost:8000/arg?location=Berkeley`, `name = request.args['name]` errors out while `name = request.args.get('name')` is executed with name being assigned the value None.

We then call our two common functions. First the `getDataFromFile()` to read all data from our json file and then `getResult()`. We return the error or the response that we talked about earlier.

### Getting data using form data

**Route: "/form"**

```
@app.route("/form", methods = ['GET'])
def getWithForm():
    name, location = request.form.get('name'), request.form.get('location')
    userLocations = getDataFromFile()
    return getResult(userLocations, name, location)
```
This endpoint functions in exactly the same way as the earlier one. We just use `request.form` to get data. The type of the output for this too is `ImmutableMultiDict` and we can process the data in the exact same manner as above.

### Getting data from file uploads

**Route: "/file"**

In the above two endpoints, we used arguments or form data to get information. However, file uploads is another really popular way to get information at the Front-End. We should also know how to process the uploaded files and also to store them.

In this lab, we will look into processing uploaded files. You can look at this [code](https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/) to understand file storage using Flask.

```
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
```
We get the uploaded file using `request.files`. The file that we are looking here should be uploaded with the key as `locationFile`. File with any other key will fail. I am using the exact same JSON as our `locations.json`. _Please note that the key for the file is not the same as filename._
We also make a check here using the `.filename` method which gives us the name of the uploaded file. We then use the `split` function using `.` as the seperator and get the extension. We then only allow for upload of JSON files and send out an error in case a file of any other type is received.

We then load the data from the uploaded file using `json.load()`. We would need to import the json module in Python for this (`import json`).
Once we have our mapping from the file, we again use our two common functions to get relevant results or return an error.