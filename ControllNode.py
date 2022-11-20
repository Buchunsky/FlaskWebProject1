import sys
from flask import Flask, request, jsonify, Response
import requests

class NodeInfo:
    def __init__(self, _count,_port, _port_to_get):
        self.count = _count
        self.port = _port
        self.port_to_get = _port_to_get

host = "127.0.0.1"
stats = {}
nodes_info = []
ports = sys.argv[1:]
port = 5001
app = Flask(__name__)

@app.route('/add', methods = ['POST'])
def add_massage():
    index = 0
    massage = request.get_json()["massage"]
    for i in range(len(nodes_info)):
        if nodes_info[index].count > nodes_info[i].count:
            index = i
    nodes_info[index].count = str(int(nodes_info[index].count)+1);
    requests.post("http://" + host + ':' + nodes_info[index].port_to_get+"/add", json={"massage":massage})
    
    return Response(200)

@app.route('/get', methods = ['GET'])
def get_massage():
    index = 0
    for i in range(len(nodes_info)):
        if nodes_info[index].count < nodes_info[i].count:
            index = i
    nodes_info[index].count = str(int(nodes_info[index].count)-1);
    r = requests.get("http://" + host + ':' + nodes_info[index].port_to_get+"/get")
    
    return r.json()


@app.route('/update', methods = ['GET'])
def update_stats():
    stats.clear()
    nodes_info.clear()
    for i in ports:
        r = requests.get("http://" + host + ':' + str(i)+"/stats")
        if r.ok:
            stats[i] = r.json()
        else:
            stats[i] = {"status" : "disabled"}
    for i in stats.keys():
        if(stats[i]["status"] == "active"):
            nodes_info.append(NodeInfo(stats[i]["ports"]["main"]["stats"], i, i))
    return jsonify({"n" :len(nodes_info)})




@app.route('/debug', methods = ['GET'])
def debug_info():
    data = {
        "stats" : stats,
        "ports" : ports
    }
    return jsonify(data)
app.run(host=host, port=port, debug=True)