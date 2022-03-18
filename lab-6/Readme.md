# Lab 6 - Asynchronous Task Queues

## Intro to Async Queues
Whatever we have learnt till now in this course has revolved around synchronous execution of tasks. However, most of the real-world processes around us are actually asynchronous. 
Think about you ordering food and the time it takes for it to arrive at your doorstep.

In the world of APIs too, a lot of processes are asynchronous. Whenever we execute a piece of code which takes some time, the execution will most likely be asynchronous.
Consider the following example:
You are building a Data Visualization platform where the flow is something like:
    1. You upload a dataset
    2. You select a few features and parameters
    3. The platform creates a visualization for you and presents it as a dashboard
Sounds cool right?

But we know that datasets are big (especially in the age we live, data is available for chump change). So it is highly likely that the data upload will take some time. Moreover, once it is uploaded, it will take some time for the data to be processed for the platform to showcase relevant features/column names etc and then there will be more time required to actually create the visualization.
So what do we do when all these processes are taking place in the background? Do we stop the user from doing anything on the platform and make them see a loader for an hour? Doesn't sound right!

This is where Asynchronous Queus come in. Asynchoronous Queues are used to store and process tasks that will take up some time while the system can move on to doing other things rather than waiting for the previous process to finish executing. Once the task has finished executing, these queues usually have a `callback` functionality which notify that the processor that the task has been executed and then the processor can do what it was supposed to do with it.

Let's think about this through another example. When you go to a restaurant to order something, does the waiter/waitress stop by your table and wait while you look at the menu and decide what you want to eat? Not unless you have questions! They will go around and serve other tables while you decide. Once you have decided, you signal or call the waiter/waitress and convey your order. The waiter/waitress then gives your order into the kitchen, who again take time to cook the food. Once the food is cooked, the waiter/waitress is called by the kitchen and then they bring you your food.

The waiter/waitress in this case is like an Async Queue while you and all the other guests at the table are tasks which are executing asynchronously. The kitchen is the processor.

## So why do we actually need Async Queues?
There are three main reasons:
<ol>
<li> <b>Speed</b>: When we’re talking to a third party API we have to face reality; unless that third party is physically located next to our infrastructure, there’s going to be latency involved. All it would take is the addition of a few API calls and we could easily end up doubling or tripling our response time, leading to a sluggish site and unhappy users. However if we push these API calls into our queue instead, we can return a response to our users immediately while our queues take as long as they like to talk to the API.</li>
</br>
<li><b>Reliability</b>: We don’t live in a world of 100% uptime, services do go down, and when they do it’s important that our users aren’t the ones that suffer. If we were to make our API calls directly in the users requests we wouldn’t have any good options in the event of a failure. We could retry the call right away in the hope that it was just a momentary glitch, but more than likely we’ll either have to show the user an error, or silently discard whatever we were trying to do. Queues neatly get around this problem since they can happily continue retrying over and over in the background, and all the while our users never need to know anything is wrong.</li>
</br>
<li><b>Scalability</b>. If we had a surge in requests that involved something CPU intensive like resizing images, we might have a problem if all of our apps were responsible for this. Not only would the increased CPU load slow down other image resize requests, it could very well slow down requests across the entire site. What we need to do is isolate this workload from the user’s experience, so that it doesn’t matter if it happens quickly or slowly. This is where queues shine. Even if our queues become overloaded, the rest of the site will remain responsive.</li>

## What is under the hood?
Queue mechanisms use something called `workers` that run in the background and take care of execution of each process in parallel. 
Task queues allow us to offload jobs to another worker process, meaning we can return something to the user immediately while the job gets placed in a queue and processed at a later time (depending on how many tasks are currently in the queue, it could start at a later time or immediately)

We have a `message broker` that acts like the middleman between our application and our workers, delivering messages when we want to schedule a task in thr queue.

We also have `producers` and `consumers` in the periphery that interact with the queue.

Using the restaurant example again, we can map all the participants as following:
1. Kitchen -> Producer
2. Customers -> Consumers
3. Restaurant Manager -> Message Broker
4. Waiter -> Workers/Task Queues

## Creating a Flask application that uses a Queue and runs it using Docker
For this task and class, we're going to use [`RQ`](https://python-rq.org/), a simple yet powerful task queue that uses Redis as a message broker.

### Installing Redis
We don't need to install Redis manually as we will be using Docker to install and run Redis, similar to when we didn't install MySQL on our computer directly but only within the container in the last lab. <i>Isn't it cool to see everything coming together now?</i>

### Creating our Flask app
We will have two Python apps - `generator.py` and `worker.py`

The Generator file is our producer which actually produces tasks to be executed.
The Worker file executes those tasks asynchronously.

#### generator.py
```
from flask import Flask, request
import json
import time
from redis import Redis
from rq import Queue
from worker import save_to_file
```
We first import `Redis` and `Queue`. We also import `save_to_file` function from our other file, i.e. `worker.py`.
We are importing `time` to simulate some delay.

```
r = Redis(host='some-redis')
queue = Queue(connection=r)
```
We now set up our own queue. We intiate a Redis instance running on `some-redis` as then host name.
We then create a queue and set the connection to be Redis instance that we just set up.

```
app = Flask(__name__)

@app.route('/start')
def start():
    i = 1
    while True:
        time.sleep(.5)
        msg = f"generator-{i}"
        print(msg)
        job = queue.enqueue(save_to_file, 'msg')
        response = {
            "jobId": job.id,
            "timeOfEnqueue": job.enqueued_at,
            "message": f"{msg} with id: {job.id} added to queue at {job.enqueued_at}"
        }
        return response, 200
```
We create a Flask app and then set up a GET endpoint called `/start`. This function uses the sleep function to simulate a delay for 0.5 seconds.
After the sleep, we just create a message `generator-{i}` where i is the count of the request sent.

`q.enqueue(function_name, args)` is used to add a task to the Queue. The `function_name` is the function that the broker will call to take care of this task -> this is essentially your worker. In our case, the worker function is `save_to_file` that we import from `worker.py`. `args` are the parameters that need to be passed to the worker function. In the above case, we pass `msg` as argument for `save_to_file`.

`job.id` and `dob.enqueued_at` are inbuild parameters that are a part of the `enqueue` function. The first one gives the unique id created for that task and the second one gives the time at which the task was queued.

#### worker.py
```
def save_to_file(msg):
    print("Processed message {msg}")
```
Our worker function - `save_to_file` is very basic and just prints the message in this case.
However, you can think of how we can use MySQL here to store data and bring in our learnings from previous labs and Assignment 1.

### Deploying via Docker
Like lab-5, we divide our working directory into two folders - `generator` and `worker` where each folder is in accordance with the coontainer that we will be running using Docker.
Both of these will have their seperate `requirements.txt` file and `Dockerfile`.

#### Docker setup for Generator

##### requirements.txt
```
flask
rq
redis
```
The `requirements.txt` file for generator include flask, rq and redis as we need all of these in our `generator.py` file.

##### Dockerfile





