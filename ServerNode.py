import sys
from flask import Flask, request, jsonify, Response
import requests

host = "127.0.0.1"
port_main = sys.argv[1]
port_rev_store_1 = sys.argv[2]
port_rev_store_2 = sys.argv[3]
port_rev_send_1 = sys.argv[4]
port_rev_send_2 = sys.argv[5]
try:
    queue_main = open(port_main+".txt", "a")
finally:
    queue_main.close()

try:
    queue_rev_1 = open(port_main+"_"+port_rev_store_1+".txt", "a")
finally:
    queue_rev_1.close()

try:
    queue_rev_2 = open(port_main+"_"+port_rev_store_2+".txt", "a")
finally:
    queue_rev_2.close()
 
app = Flask(__name__)


@app.route('/add', methods = ['POST'])
def add_massage():
    incomming = request.get_json()
    with open(port_main+".txt", 'a') as f:
        f.write(incomming["massage"]+"\n")
    add_rev(incomming["massage"])
    return Response(status=200)

@app.route('/get', methods = ['GET'])
def get_massage():
    with open(port_main+".txt", 'r') as f:
        data = f.read().splitlines(True)
        if len(data) != 0:
            delete_from_rev()
            with open(port_main+".txt", 'w') as fout:
                fout.writelines(data[1:])
            return jsonify({"massage" : data.pop(0)})
        return Response(status=404)

@app.route('/getrev1', methods = ['GET'])
def get_massage_rev1():
    with open(port_main+"_"+port_rev_store_1+".txt", 'r') as f:
        data = f.read().splitlines(True)
        if len(data) != 0:
            delete_from_rev()
            with open(port_main+"_"+port_rev_store_1+".txt", 'w') as fout:
                fout.writelines(data[1:])
            return jsonify({"massage" : data.pop(0)})
        return Response(status=404)

@app.route('/getrev2', methods = ['GET'])
def get_massage_rev2():
    with open(port_main+"_"+port_rev_store_2+".txt", 'r') as f:
        data = f.read().splitlines(True)
        if len(data) != 0:
            delete_from_rev()
            with open(port_main+"_"+port_rev_store_2+".txt", 'w') as fout:
                fout.writelines(data[1:])
            return jsonify({"massage" : data.pop(0)})
        return Response(status=404)

@app.route('/delete', methods = ['POST'])
def delete_massage():
    incomming = request.get_json()
    port_to_del = str(incomming["port"])
    if (port_to_del == str(port_rev_store_1)):
        with open(port_main+"_"+port_rev_store_1+".txt", 'r') as fin:
            data = fin.read().splitlines(True)
        with open(port_main+"_"+port_rev_store_1+".txt", 'w') as fout:
            fout.writelines(data[1:])
        return Response(status=200)
    elif (port_to_del == str(port_rev_store_2)):
        with open(port_main+"_"+port_rev_store_2+".txt", 'r') as fin:
            data = fin.read().splitlines(True)
        with open(port_main+"_"+port_rev_store_2+".txt", 'w') as fout:
            fout.writelines(data[1:])
        return Response(status=200)
    else:
        return Response(status=404)



@app.route('/addrev', methods = ['POST'])
def add_rev_massage():
    incomming = request.get_json()
    port_to_add = str(incomming["port"])
    if (port_to_add == str(port_rev_store_1)):
        with open(port_main+"_"+port_rev_store_1+".txt", 'a') as f:
            f.write(incomming["massage"]+"\n")
        return Response(status=200)
    elif (port_to_add == str(port_rev_store_2)):
        with open(port_main+"_"+port_rev_store_2+".txt", 'a') as f:
            f.write(incomming["massage"]+"\n")
        return Response(status=200)
    else:
        return Response(status=404)


@app.route('/stats', methods = ['GET'])
def stats():
    m = open(port_main+".txt", 'r').readlines()
    r1 = open(port_main+"_"+port_rev_store_1+".txt", 'r').readlines()
    r2 = open(port_main+"_"+port_rev_store_2+".txt", 'r').readlines()
    data = {
        "status" : "active",
        "ports":
        {
            "main":
            {
                "port" : port_main,
                "stats" : str(len(m))
            },
            "rev1":
            {
                "port" : port_rev_store_1,
                "stats" : str(len(r1))
            },
            "rev2":
            {
                "port" : port_rev_store_2,
                "stats" : str(len(r2))
            },
        }
    }
    return jsonify(data)

def delete_from_rev():
    requests.post("http://" + host + ':' + port_rev_send_1+"/delete", json = {"port" : port_main})
    requests.post("http://" + host + ':' + port_rev_send_2+"/delete", json = {"port" : port_main})

def add_rev(massage):
    requests.post("http://" + host + ':' + port_rev_send_1+"/addrev", json = {"port" : port_main, "massage" : massage})
    requests.post("http://" + host + ':' + port_rev_send_2+"/addrev", json = {"port" : port_main, "massage" : massage})

@app.route('/debug', methods = ['GET'])
def debug_info():
    data = {
        "port_main" : port_main,
        "port_rev_store_1" : port_rev_store_1,
        "port_rev_store_2" : port_rev_store_2,
        "port_rev_send_1" : port_rev_send_1,
        "port_rev_send_2" : port_rev_send_2
    }
    return jsonify(data)


app.run(host = host, port = port_main, debug = True)