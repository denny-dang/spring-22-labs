# Step 1 — Setting up the Database

First, we set up the SQLite database (sqlite3 module) to store and retrieve our data

Data in SQLite is stored in tables and columns, so we first need to create a table called cats with the necessary columns. We create a .sql file that contains SQL commands to create the cats table with a few columns. We then use this schema file to create the database.

Open a database schema file called `schema.sql` inside our `cats_app` directory:

```
nano schema.sql
```

In this schema file, we first delete the cats table if it already exists. This avoids the possibility of another table named cats existing, which might result in confusing behavior (for example, if it has different columns).

```
DROP TABLE IF EXISTS cats;

CREATE TABLE cats (
    id varchar(500) PRIMARY KEY,
    catName varchar(500) NOT NULL,
    catColor varchar(500) NOT NULL,
    catBreed varchar(500) NOT NULL
);
```

We use `CREATE TABLE` cats to create the `cats` table with the following columns:
    1. `id`: We use UUIDs here to generate unique ids for each of our cat. We use the `uuid` module from Python for the same.
    2. `catName`: A column that takes in NON NULL text values to store the name of each cat.
    3. `catColor`: A column that takes in NON NULL text values to store the color of each cat.
    4. `catBreed`: A column that takes in NON NULL text values to store the breed of each cat.

Now, we'll use the `schema.sql` file to create the database. To do so, we’ll create a Python file that will generate an SQLite .db database file based on this `schema.sql` file. Open a file named `init_db.py` inside our `cats_app` directory.

```
nano init_db.py
```
Now we ddd the following code to our file:

```
import sqlite3
import uuid

newCatId = str(uuid.uuid4())

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO cats (id, catName, catColor, catBreed) VALUES (?, ?, ?, ?)",
            (newCatId, 'Fluffy', 'Black', 'Ragdoll',)
            )

connection.commit()
connection.close()
```

We first import the `sqlite3` module. We open a connection to a database file named `database.db`, which will be created once we run the Python file. Then we use the `open()` function to open the schema.sql file. Next we execute its contents using the `executescript()` method that executes multiple SQL statements at once, which will create the cats table. we create a Cursor object that allows we to process rows in a database. In this case, we’ll use the cursor’s `execute()` method to execute INSERT SQL statement to add a cat to our cats table. Finally, we commit the changes and close the connection.

Save and close the file and then run it in the terminal using the python command:

```
python3 init_db.py
```

Once the file finishes execution, a new file called database.db will appear in our flask_app directory. This means we’ve successfully set up wer database.

Next, we’ll create a small Flask application, retrieve the two cats we inserted into the database, and display them on the index page.

# Step 2 — Inserting new cats in the Database

We create our server file that uses Flask

```
nano app.py
```
Within the `app.py` file, we add the following code:

```
from crypt import methods
import sqlite3
from flask import Flask, Response, request
import uuid

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['POST'])
def index():
    conn = get_db_connection()
    cat = request.get_json()
    try:
        conn = get_db_connection()
        newCatId = str(uuid.uuid4())
        catName, catColor, catBreed = cat['catName'], cat['catColor'], cat['catBreed']
        conn.execute('INSERT INTO cats (id, catName, catColor, catBreed) VALUES (?, ?, ?, ?)',
                        (newCatId, catName, catColor, catBreed))
        conn.commit()
        conn.close()
        return {'cat': {
            'id': newCatId,
            'catName': cat['catName'],
            'catColor': cat['catColor'],
            'catBreed': cat['catBreed']
        }, 'message': 'Cat inserted with id: '+newCatId }, 201
    except:
        return {'error': 'Invalid JSON Body', 'status': 400}, 400

```
In the code above, as you see, we are importing multiple libraries. We will learn more about them as an when we use it. We first import the sqlite3 module to use it to connect to our database. We make a Flask application instance called app. We define a function called `get_db_connection()`, which opens a connection to the database.db database file we created earlier, and sets the `row_factory` attribute to `sqlite3.Row` so we can have name-based access to columns. This means that the database connection will return rows that behave like regular Python dictionaries. Lastly, the function returns the conn connection object you’ll be using to access the database.

We then use the app.route() decorator to create a Flask view function called `index()`. We use the `get_db_connection()` function to open a database connection. 

The next task is to get cat data from the JSON body of our request. We hence use the `request.get_json()` to do that. We then reference the key values from our body - `catName`, `catColor` and `catBreed`
Now since we are inserting into a SQL database, we need a unique id that will be set as the primary key. To do that we are using the uuid module from python which gives us a unique key that we can use here as our primary key.
Finally we use the `execute()` function to `INSERT INTO` our cats table using all the values that we got from out body.

We then return a JSON response with a status code 201 if the insert was successful. In case we had missing values from the body, we raise an error and return an error message alongside a 400 status code.

We use the Response from Flask library to create a JSON response for our API with a status code and application type

# Step 3 — Getting all cats from the Database

We can use the same route as above to get all the cats stored in the database.
We do that by adding `GET` as a method in our `app.route()`

The updated code would look something like this:

```
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    if request.method == 'POST':
        cat = request.get_json()
        try:
            conn = get_db_connection()
            newCatId = str(uuid.uuid4())
            catName, catColor, catBreed = cat['catName'], cat['catColor'], cat['catBreed']
            conn.execute('INSERT INTO cats (id, catName, catColor, catBreed) VALUES (?, ?, ?, ?)',
                         (newCatId, catName, catColor, catBreed))
            conn.commit()
            conn.close()
            return {'cat': {
                'id': newCatId,
                'catName': cat['catName'],
                'catColor': cat['catColor'],
                'catBreed': cat['catBreed']
            }, 'message': 'Cat inserted with id: '+newCatId }, 201
        except:
            return {'error': 'Invalid JSON Body', 'status': 400}, 400
    else:
        cats = conn.execute('SELECT * FROM cats').fetchall()
        print('Type: ', cats)
        conn.close()
        catList = list()
        for cat in list(cats):
            catList.append({
                'id': cat['id'],
                'catName': cat['catName'],
                'catColor': cat['catColor'],
                'catBreed': cat['catBreed']
            })
        return {'data': catList}, 200
```
We use the `request.method` to check if our request is a GET request or a POST request. If it was a POST request, we route it to do what we did in Step 2 above.

For the GET call, we are executing a `SELECT` query using the `fetchall()` function that gets all the cats in the `cats` table. We iterate over this response and add each cat into our `catList` which is then returned as part of the response with a 200 status code.
For each cat in the response, we are creating a JSON body that includes its id, name, color and breed.

# Step 4 — Getting a cat from the Database using its ID

We create a new GET route that accepts an id as part of the URL param. This id references a cat in the database.

The code for this route would look something like

```
@app.route('/<string:id>/', methods=['GET'])
def getById(id):
    conn = get_db_connection()
    cat = conn.execute('SELECT * FROM cats WHERE id = ?',
                        (id,)).fetchone()
    conn.close()
    if cat is None:
        return {'error': 'Invalid ID', 'status': 400}, 400
    return {'cat': {
                'id': cat['id'],
                'catName': cat['catName'],
                'catColor': cat['catColor'],
                'catBreed': cat['catBreed']
            }}, 200
```

In the route, we specify `string:id` which tells the app to expect a URL param of type string in the request. Now that `id` is used to search
for that cat in the database.
We use the `SELECT` command again but with a `WHERE` clause this time and the `fetchone()` function to just get one record as part of the response.
Like in the GET ALL API, we reconfigure this data into a JSON and send it as the response with a status code 200.
In case we didn't find any cat with that id aka your query result was empty, we return an error with a 400 status code.

# Parting Notes
- We saw how to set up a database connection between our `Flask server` and `SQLlite3`. We created a new table using an SQL schema.
- We also created 3 routes to interact with our server - POST, GET all, GET by ID.
- We interacted with JSON body and URL params to process the API requests and responded using clean JSON responses with valid status code.
- We also learnt how to test our API using tools like POSTMAN.