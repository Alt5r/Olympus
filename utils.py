import requests 
import json




def Req_proxy():
    """
    returning socks4,5 proxies that have had a < 40% success rate when used and returning the connection data in a list
    """
    url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=socks5,socks4&proxy_format=protocolipport&format=json&anonymity=Elite,Anonymous&timeout=9810"

    data = requests.get(url).json()
    #print(data)
    proxiesLst = data["proxies"]
    #print(proxiesLst[0])
    i=0

    proxiesLstFilt = []
    for p in proxiesLst:
        if p["uptime"] >= 40:
            i+= 1
            proxiesLstFilt.append(p)
    
    print(f"{i} proxies appended to list")
    
    #just connection details
    finalLst = []
    for proxy in proxiesLstFilt:
        finalLst.append(proxy["proxy"])
    return finalLst, i

    #

def geonode_proxies():
    url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
    data = requests.get(url).json()

    proxyFilt = []

    for p in data["data"]:
        if p['latency'] <= 50:
            num = p["upTime"] 
            if num > 90:
                proxyFilt.append(p)

    #print(proxyFilt)

    proxiesFinal = []
    i=0
    for p in proxyFilt:
        proxiesFinal.append(f"{p['protocols'][0]}://{p['ip']}:{p['port']}")
        i+=1
    return proxiesFinal, i
    """
    returning socks proxies for geonode service
    """

def tester(proxy):
    p = {
        'http':f"{proxy}",
        'https':f"{proxy}"
    }

    test_url = "http://httpbin.org/ip"

    try:
        # Make a request through the SOCKS proxy
        response = requests.get(test_url, proxies=proxy, timeout=5)
        response.raise_for_status()  # Check if the request was successful
        print("SOCKS proxy is working. Your IP is:", response.json()["origin"])
        return True
    except requests.exceptions.RequestException as e:
        print("SOCKS proxy failed:", e)
        return False
    
