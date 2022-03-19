from flask import Flask
import time
from redis import Redis
from rq import Queue
from rq.job import Job
from worker import save_to_file
import random

r = Redis(host='redis', port=6379, decode_responses=True)
queue = Queue(connection=r)

app = Flask(__name__)

@app.route('/start')
def start():
    
    delayTime = random.randint(1,10)
    time.sleep(delayTime)
    msg = f"generating task with delay: {delayTime}"
    print(msg)
    job = queue.enqueue(save_to_file, msg)
    response = {
            "jobId": job.id,
            "timeOfEnqueue": job.enqueued_at,
            "message": f"{msg} with id: {job.id} added to queue at {job.enqueued_at}"
        }
    print(response) 

if __name__ == '__main__':
    app.run(host='0.0.0.0')



