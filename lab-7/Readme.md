# Lab 7 - Asynchronous Task Queues

## Intro to NoSQL Datbases
In today's lab we covered the basics of NoSQL databases, how they are different to RDBMS/SQL databases like MySQL we have used in the past.
We then proceeded to create a NoSQL database on cloud using [MongoDB Atlas](cloud.mongodb.com) which allows setting up free shared clusters online.
You can create an account, and create a new cluster with a username and password.
We will then use this cluster alongside its authentication mechanisms for connecting our application to the database.

Our database and the collection will be hosted within this cluster.

For people who are interested in diving deeper into NoSQL databases, this [link](https://www.mongodb.com/nosql-explained/nosql-vs-sql) might be helpful. And this is a quick [intro](https://www.guru99.com/nosql-tutorial.html#:~:text=NoSQL%20Database%20is%20a%20non,and%20real%2Dtime%20web%20apps.) to NoSQL databases.

## Connecting to our MongoDB Cluster
Before we begin, please install `pymongo` and `pymongo[srv]` using `pip3 install pymongo` and `pip3 install "pymongo[srv]"`.

```
# Like we did in our MySQL webserver files, we create a function that connects to MongoDB
def mongoConnection():
    try:
        # change your <username> and <password> below to connect to the database
        client = pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0.0yqkv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client["test"] # Name of your database
        col = db["testCol"] # Name of your collection
        return col
    except:
        return Exception('Error connecting to DB')
```
We set up a client using pymongo's MongoClient. The URL in this line can be obtained using your MongoDB atlas dashboard. There should be a `connect` button right next to your cluster which should give you this URL and relevant commands for Python.

<strong>Please change your username and password in this line to reflect your credentials.

We then connect to our database using `client['test']` where `test` is the name of the database and to our collection within that database using `db['testCol']` where `testCol` is the name of our collection.

## Using NoSQL/MongoDB instead of MySQL
The setup of the Flask webapp will exactly be the same as we have done throughout this course at various instances. However, the way we interact with MongoDB for CRUD operations is a bit different

### Insertion into MongoDB
Since MongoDB (NoSQL databases in general) uses an object model, we create a JSON object for our resource and then use that for insertion. We don't insert anything into a table based on a fixed schema.

```
params = request.get_json()
title = params['title']
status = params['status']
record = {
    "title": title,
    "status": status
    }
res = col.insert_one(record)
return {}, 201    
```
We first create `record` object using our parameters we got from our JSON body and then we use `insert_one` command to insert our record into the collection.

### Querying from MongoDB
<ol>
<li> Query all records</li>
To query all records, we use `col.find({})` where `col` is our collection

```
tasks = col.find({})
```

We then use an iterator to convert this reponse into a list of object that is suitable and readable for return.

```
output = list()
for task in tasks:
    output.append({"id": str(task["_id"]),
    "title": task["title"],
    "status": task["status"]})
return {"result": output}, 200
```
<li> Query filtered records</li>
To query a record based on a certain parameter or condition, we can directly embed our condition into the `find()`.

```
task = col.find_one({"title": title})
```
Here, we are filtering our results based on the `title`. Please note that the filters you provide are keys within your objects in the collection.

