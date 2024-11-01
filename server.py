from flask import Flask, request, jsonify
from utils import *
import random

app = Flask(__name__)

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


@app.route('/api/S5', methods=['GET'])
def get_data5():
    """
    returning 5 random proxies from source, for smaller scale operations maybe
    """
    data = scraperCall()
    
    lst5 = []
    for i in range(5):
        rand = random.randint(0,len(data["proxies"]))
        lst5.append(data["proxies"][rand])
    
    sample_data = {"n0":5, "proxies":lst5}

    return jsonify(sample_data)

if __name__ == '__main__':
    app.run(debug=True)