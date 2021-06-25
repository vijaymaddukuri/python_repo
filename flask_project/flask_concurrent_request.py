from flask import Flask, Response
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import requests
import json

# DOCS https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=2)

app = Flask(__name__)


@app.route('/jobs', methods=['POST'])
def run_jobs():
    executor.submit(some_long_task1)
    executor.submit(some_long_task2, 'hello', 123)
    return 'Two jobs were launched in background!'


def some_long_task1():
    print("Task #1 started!")
    sleep(10)
    print("Task #1 is done!")


def some_long_task2(arg1, arg2):
    print("Task #2 started with args: %s %s!" % (arg1, arg2))
    sleep(5)
    res = requests.post("http://0.0.0.0:80/new")
    print(res.status)
    print("Task #2 is done!")


@app.route('/new', methods=['POST'])
def second_task():
    print("Came to second endpoint \n")
    print(requests)
    return Response("{'a':'b'}", status=201, mimetype='application/json')


def start_server(portnumber):
    app.run(debug=True, host='0.0.0.0', port=portnumber)


if __name__ == '__main__':
    start_server(80)