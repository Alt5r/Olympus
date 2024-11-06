from flask import Flask, request, jsonify
from utils import *
import threading
import random
from datetime import datetime
import time 
import requests

app = Flask(__name__)

global data

data = {'n0':0, 'proxies':[]}

global gitdata4

gitdata4 = {'n0':0, 'proxies':[]}

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
    #data = scraperCall()
    number = data['n0']
    dist = {
        "socks4":0, 
        "socks5":0,
        "http":0,
        "gitlist":{
            "socks4":0,
            "socks5":0
        }
    }

    for proxy in data["proxies"]:
        if "socks4" in proxy:
            dist["socks4"] += 1
        elif "socks5" in proxy:
            dist["socks5"] += 1
        else:
            dist["http"] += 1
    try:
        dist['gitlist']["socks4"] = len(gitdata4['proxies'])
    except Exception as e:
        print(e)

    data2 = {
        "uptime":uptime,
        "number":number,
        "dist":dist
    }
    print(f"{data}\n\n\n\n")
    print(gitdata4)
    return data2


@app.route('/api/v1', methods=['GET'])
def get_data5():
    """
    returning 5 random proxies from source, for smaller scale operations maybe

    using query string parameters
    """
    args = request.args
    print(args)
    noResults = int(args['amount'])
    #global data
    #data = scraperCall()
    
    lst5 = []
    for i in range(noResults):
        rand = random.randint(0,len(data["proxies"])-1)
        lst5.append(data["proxies"][rand])
    
    sample_data = {"n0":noResults, "proxies":lst5}

    return jsonify(sample_data)

def testingd():
    global data

    proxyt = ""
    while True:
        try:
            for proxy in data['proxies']:
                proxyt = proxy
                if tester(proxy) == True:
                    print(f"SOCKS/HTTP proxy working: {proxy}")
                elif tester(proxy) == False:
                    
                    data['proxies'].remove(proxyt)
                    data['n0'] -= 1
                    print(f"SOCKS/HTTP proxy failed: {proxyt}")
                #time.sleep(2)
        except Exception as e:
            #print(data['proxies'])
            print(e)
            #print('data prolly empty')
            data['proxies'].remove(proxyt)
            data['n0'] -= 1
            #print(f"{proxyt} is not working")
        #time.sleep(2)

def scraperd():
    #runs getting the github proxy list once per run | to change
    gitdata4['proxies'] = gitproxies4()
    while True:
        global data
        data = scraperCall()
        print(f"pulled proxies {datetime.now()}")
        time.sleep(600)

def gitproxies4d():
    '''
    daemon to filter throuhg ~2700 proxies from socks4 list on github and append working ones to data var

    '''
    global data
    #the above to allow changing global var

    while True:
        try:
            for proxy in gitdata4['proxies']:
                
                if tester(proxy) == True:
                    #print(f"{proxy} is working | Git proxies SOCKS4")
                    data['proxies'].append(proxy)
                    print("\n\nproxy appended\n\n")
                    data['n0'] += 1
                else:
                    #print(f"{proxy} doesnt work | git proxies SOCKS4")
                    pass
                #time.sleep(2)
        except Exception as e:
            print(e, "error occured in try function for git proxies SOCKS4")

if __name__ == '__main__':
    data = scraperCall()

    # thread for pulling proxies from sources
    scrapert = threading.Thread(target=scraperd)
    scrapert.daemon = True
    scrapert.start()

    #daemon thread for filtering SOCKS4 proxies from github list
    """
    filterd = threading.Thread(target=gitproxies4d)
    filterd.daemon = True
    filterd.start()
    """




    start = datetime.now()
    #thread for filtering pulled proxies 
    thread = threading.Thread(target=testingd)
    thread.daemon = True
    thread.start()

    app.run(debug=True)
    