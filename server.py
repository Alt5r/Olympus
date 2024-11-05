from flask import Flask, request, jsonify
from utils import *
import threading
import random
from datetime import datetime

app = Flask(__name__)

data = {}

def scraperCall():
    """
    collecting all proxies from all sources and returning into array
    """
    p = Req_proxy()
    q = geonode_proxies()
    p[0].extend(q[0])
    #print(p[1])
    #p[1] += len(q)
    d = p[1] + q[1]
    sample_data = {"n0": d, "proxies": p[0]}
    return sample_data

# Example GET route
@app.route('/api/Sall', methods=['GET'])
def get_data():
    return jsonify(scraperCall())

@app.route('/api/info', methods=['GET'])
def get_info():
    uptime = ((datetime.now() - start).seconds)/60 # uptime in minutes
    data = scraperCall()
    number = data['n0']
    dist = {
        "socks4":0, 
        "socsk5":0,
        "http":0
    }

    for proxy in data["proxies"]:
        if "socks4" in proxy:
            dist["socks4"] += 1
        elif "socks5" in proxy:
            dist["socsk5"] += 1
        else:
            dist["http"] += 1

    data = {
        "uptime":uptime,
        "number":number,
        "dist":dist
    }
    return data


@app.route('/api/v1', methods=['GET'])
def get_data5():
    """
    returning 5 random proxies from source, for smaller scale operations maybe

    using query string parameters
    """
    args = request.args
    print(args)
    noResults = int(args['amount'])
    
    data = scraperCall()
    
    lst5 = []
    for i in range(noResults):
        rand = random.randint(0,len(data["proxies"]))
        lst5.append(data["proxies"][rand])
    
    sample_data = {"n0":noResults, "proxies":lst5}

    return jsonify(sample_data)

def testingd():
    try:
        for proxy in data[1]:
            if tester(proxy):
                print(f"{proxy} is working")
            else:
                data[1][proxy].remove()
                print(f"{proxy} is not working")
    except Exception as e:
        print(e)
        print('data prolly empty')


if __name__ == '__main__':
    thread = threading.Thread(target=testingd)
    thread.daemon = True
    thread.start()

    app.run(debug=True)
    