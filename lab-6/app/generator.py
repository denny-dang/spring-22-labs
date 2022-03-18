from flask import Flask, request
import worker
import json
import time
from redis import Redis
from rq import Queue
import sys


r = Redis(host='redis', port=6379, decode_responses=True)
queue = Queue(connection=r)
app = Flask(__name__)

@app.route('/start')
def start():
    print('Here')
    i = 1
    while True:
        time.sleep(.5)
        msg = f"generator-{i}"
        print(msg)
        job = queue.enqueue(worker.save_to_file, 'msg')
        response = {
            "jobId": job.id,
            "timeOfEnqueue": job.enqueued_at,
            "message": f"{msg} with id: {job.id} added to queue at {job.enqueued_at}"
        }
        print(response)

    




