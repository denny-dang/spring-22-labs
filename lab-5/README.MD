# Lab 5 - Deep dive into Docker and Docker Compose

In today's lab, we deep-dive into Docker and Docker Compose.
We run two different containers - one for our Flask webserver and one for the MySQL database.

We create a Docker Image file for our Flask webserver while we pull a pre-defined one from the Docker Library for MySQL. 

Based on what we learnt on Monday, we can run a docker container using an image file using `docker run` command. But that becomes tedious and difficult to manage, especially if you have too many containers to run concurrently or if each of these requires extensive configurations like Port Numbers, User Access information, Storage Access etc.

To streamline the process of running multiple docker containers together, we use `Docker Compose`. As the name suggest, we compose the imformation of all our containers in a `docker-compose yaml` file which goes by the `.yml` extension.

## Setting up our repository
First, we will create our repo in a structured way so that it is easier to maintain and use in the long-term.

Since, we have two major components - the Flask app and the MySQL db, we create two different folders - one called `app` and the other called `db`.

The main directory will also host our `docker-compose.yml` file which will make use of both these folders that we created above to run our Python app and the MySQL database in two seperate containers.

Before we get into setting up our Docker Compose file and working with images, we need to set up our database and the Flask webserver.

## Creating our database and the table
We need to create a `.sql` file that will enable us to create our Database and the table within it that we will be using.

We first create a new database using the `CREATE DATABASE` command and we name it `catsdb`. Then we create a new table called `cats` and insert two new rows into it. 

## Creating our Flask app
We initialize a very basic Flask app that only has one `GET` call for now and displays all the data within the MySQL table.

```
@app.route('/')
def index() -> str:
    js = json.dumps(getCats())
    resp = Response(js, status=200, mimetype='application/json')
    return resp
```
Above is our `GET` index route which calls the `getCats()` function and then converts the response into an ideal JSON format and then returns it as the API response.

```
def getCats() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'catsdb'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM cats')
    result = cursor.fetchall()

    cursor.close()
    connection.close()
    return result
```
The config is what we are using to connect our Python application to the MySQL server.

We are connecting as `root` with the password configured in the docker-compose file. Notice that we explicitly define the host (which is localhost by default) since the SQL service is actually in a different container than the one running this code. We can (and should) use the name ‘db’ since this is the name of the service we defined and linked to earlier, and the port is 3306 and not 32000 since this code is not running on the host.

Next is initializing the connection using `mysql.connector` and pointing out our config, getting the cursor and then executing our `SELECT *` query for the response.

## Creating the Docker Image for our Python app
A Dockerfile contains a set of instructions describing our desired image and allow its automatic build.

```
# Use an official Python runtime as an image
FROM python:3.8

# The EXPOSE instruction indicates the ports on which a container 
# will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 5000

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this instruction 
# creates a directory with this name if it doesn’t exist
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Run app.py when the container launches
COPY app.py /app
CMD python app.py
```
What this does is simply as described in the file — base the image on a Python 3.8 image, expose port 5000 (for Flask), create a working directory to which requirements.txt and app.py will be copied, install the needed packages and run the app.

We need our dependencies (Flask, mysql-connector and simplejson) to be installed and delivered with the image, so we need to create the aforementioned requirements.txt file:

```
Flask
mysql-connector
simplejson
```

Now we can create a docker image for our app, but we still can’t use it, since it depends on MySQL, which, as good practice commens, will reside in a different container. 

Hence, we will use docker-compose to facilitate the orchestration of the two independant containers into one working app.

## Creating our Docker-Compose file
So let’s create a new file, docker-compose.yml, in our project’s root directory:
```
version: "2"
services:
  app:
    build: ./app
    container_name: "Flask_App"
    links:
      - db
    ports:
      - "8000:5000"
```
We are using two services, one is a container which exposes the REST API (app), and one contains the database (db).

<ul>
<li>build: specifies the directory which contains the Dockerfile containing the instructions for building this service
<li>container name: specifies the name of the container when it is finally deployed
<li>links: links this service to another container. This will also allow us to use the name of the service instead of having to find the ip of the database container, and express a dependency which will determine the order of start up of the container
<li>ports: mapping of <Host>:<Container> ports. So here, our POSTMAN will call the docker container (our application host) at port 8000 but the container in itself is running the Flask app on 5000.
</ul>

```
db:
    image: mysql:5.7
    platform: linux/amd64
    container_name: "MySQL_Database"
    ports:
      - "32000:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root
    volumes:
      - ./db:/docker-entrypoint-initdb.d/:ro
```
<ul>
<li>image: Like the FROM instruction from the Dockerfile. Instead of writing a new Dockerfile, we are using an existing image from a repository. It’s important to specify the version — if your installed mysql client is not of the same version problems may occur.
<li>platform: Only to be used if you are using a Mac M1 chip as it is not ARM based.
<li>environment: add environment variables. The specified variable is required for this image, and as its name suggests, configures the password for the root user of MySQL in this container. More variables are specified here.
<li>ports: Since I already have a running mysql instance on my host using this port, I am mapping it to a different one. Notice that the mapping is only from host to container, so our app service container will still use port 3306 to connect to the database.
<li>volumes: since we want the container to be initialized with our schema, we wire the directory containing our init.sql script to the entry point for this container, which by the image’s specification runs all .sql scripts in the given directory.
</ul>

We are now ready to start the dockerized app!

## Running the Docker containers
We can use `docker-compose up` or `docker-compose up -d` to start our docker containers. Please note that running this command for the first time will be time taking.

Use `ctrl + c` to exit and pause the container. You can use `docker-compose down` to delete the container. Note that this only deletes the containers and doesn't delete the images. These images once pulled/created are saved so that your containers can be started quickly in the future.




