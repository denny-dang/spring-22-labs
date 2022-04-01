from crypt import methods
import unicodedata
from flask import Flask, request
import time
from redis import Redis
from rq import Queue
from rq.job import Job
from worker import save_to_file
import random
from rq.registry import StartedJobRegistry

r = Redis(host='redis', port=6379)
queue = Queue(connection=r)

app = Flask(__name__)

@app.route('/start')
def start():
    
    delayTime = random.randint(20,30)
    msg = f"generating task with delay: {delayTime}"
    job = queue.enqueue(save_to_file, msg, delayTime)
    response = {
            "jobId": job.id,
            "timeOfEnqueue": job.enqueued_at,
            "message": f"{msg} with id: {job.id} added to queue at {job.enqueued_at}"
        }
    return response

@app.route('/list')
def getList():
    registry = StartedJobRegistry('default', connection=r)
    running_job_ids = registry.get_job_ids()  # Jobs which are exactly running. 
    return {"jobs": running_job_ids}

@app.route('/status/<id>')
def getStatus(id):
    job = Job.fetch(id, connection=r)
    return {"result": job.result}

if __name__ == '__main__':
    app.run(host='0.0.0.0')



