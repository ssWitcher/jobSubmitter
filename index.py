import flask
import Queue
from threading import Thread
from flask import request, jsonify
import uuid

from jobSumitter import submitJob


app = flask.Flask(__name__)
q = Queue.Queue(maxsize=0)

@app.route('/api/render', methods=['POST'])
def read_req():
    payload = request.get_json(force=True)
    input_file_path = payload["input_file_path"]
    print("=====================")
    print(payload)
    print("===================")
    print("=====================")
    print(input_file_path)
    print("===================")
    output_file = input_file_path.split("/")[-1]+"_"+uuid.uuid4()
    worker(q)
    q.put({"input_file_path":input_file_path,"output_file":output_file})
    return "Added to queue"



def worker(q):
    worker = Thread(target=submitJob, args=(q,))
    worker.setDaemon(True)
    worker.start()


if __name__ == "__main__":
    app.run(host='0.0.0.0',threaded=True,port=5000)