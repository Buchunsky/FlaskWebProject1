from http import server
import json
from multiprocessing import Process
import this
import threading

class Controller:
    def __init__(self):
        pass
    

class DataNodeInfo:
    def __init__(self, _status, _port):
        self.status = _status
        self.port = _port

class Handler(server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/":
            self.send_response(200)
            self.end_headers()

            request_body_json_string = "Hello empty"
            json_data_obj = json.loads(request_body_json_string)
            json_data_obj['SEEN_BY_THE_SERVER'] = 'Yes'
            self.wfile.write(bytes(json.dumps(json_data_obj), 'utf-8'))

        if self.path == "/jack/":
            self.send_response(200)
            self.end_headers()

            request_body_json_string = "Hello jack"
            json_data_obj = json.loads(request_body_json_string)
            json_data_obj['SEEN_BY_THE_SERVER'] = 'Yes'
            self.wfile.write(bytes(json.dumps(json_data_obj), 'utf-8'))
        pass

class DataNode():
    def __init__(self, port):
        self.run(port)
    def run(port, server_class=server.HTTPServer, handler_class=Handler):
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        threading.Thread(target=server_class.serve_forever).start()

class UserController:
    def __init__(self):
        pass
    




