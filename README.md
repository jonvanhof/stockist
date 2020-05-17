# stockist
_A lightweight data aggregation and presentation library_

### Installation

##### Set up virtual environment and install required libraries
````
$ python3 -m venv .
$ . bin/activate
$ pip install -r requirements.txt
````

### Usage

##### Create a new Stockist instance
````
import stockist
from flask import Flask
from flask_cors import CORS


stk = stockist.Stockist('demo')
````

##### Define fields and add an object
````
emp_fields = {'emp_id': 'int pk',
              'name': 'string',
              'position': 'string'}
stk.add_object('employee', emp_fields, 0)
````

##### Add a source
````
sample_base_url = "http://sample.com/rest"
stk.add_source('employee', 'json', sample_base_url)
````

##### Define a Stock Request with path and query mapping function
````
query_path = "get_employee'"

def qry_func(res_dict):
    ret_rows = []
    for i in res_dict:
        ret_dict = {'emp_id': i['id'],
                    'name': i['employee_name'],
                    'position': i['role']}
    return ret_dict

stk.add_stock_request(stk.sources[0], stk.objects[0], query_path, qry_func)
````

##### Stock the database from source
````
stk.stock_requests[0].stock()
````

##### Add one or more endpoints
````
stk.add_endpoint("emp", stk.objects[0])
````

##### Create a Flask App and create endpoint map
````
stk_app = Flask(__name__)
CORS(stk_app)
stk.create_endpoints(stk_app)
````

### Launch App Server
````
$ gunicorn demo:stk_app
[INFO] Starting gunicorn 20.0.4
[INFO] Listening at: http://127.0.0.1:8000 (70518)
[INFO] Using worker: sync
[INFO] Booting worker with pid: 70521
````
