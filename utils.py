import requests 
import json
import random
from fake_headers import Headers
global sites

sites = [
    "www.google.com",
    "www.example.com",
    "www.yahoo.com",
    "www.microsoft.com",
    "www.facebook.com",
    "www.instagram.com",
    "www.twitter.com",
    "www.amazon.com",
    "www.netflix.com",
    "www.reddit.com",
    "www.wikipedia.org",
    "www.apple.com",
    "www.linkedin.com",
    "www.github.com",
    "www.stackoverflow.com",
    "www.spotify.com",
    "www.dropbox.com",
    "www.pinterest.com",
    "www.tumblr.com",
    "www.airbnb.com",
    "www.bing.com",
    "www.ebay.com",
    "www.paypal.com",
    "www.aliexpress.com",
    "www.cnn.com",
    "www.nytimes.com",
    "www.bbc.com",
    "www.theguardian.com",
    "www.washingtonpost.com",
    "www.nike.com",
    "www.adidas.com",
    "www.coursera.org",
    "www.udemy.com",
    "www.skillshare.com",
    "www.khanacademy.org",
    "www.salesforce.com",
    "www.oracle.com",
    "www.ibm.com",
    "www.huawei.com",
    "www.samsung.com",
    "www.hp.com",
    "www.dell.com",
    "www.intel.com",
    "www.amd.com",
    "www.tesla.com",
    "www.ford.com",
    "www.gm.com",
    "www.toyota.com",
    "www.honda.com",
    "www.chevrolet.com",
    "www.mercedes-benz.com",
    "www.bmw.com",
    "www.nbcnews.com",
    "www.foxnews.com",
    "www.aljazeera.com",
    "www.reuters.com",
    "www.bloomberg.com",
    "www.forbes.com",
    "www.time.com",
    "www.wsj.com",
    "www.espn.com",
    "www.si.com",
    "www.cbssports.com",
    "www.yelp.com",
    "www.tripadvisor.com",
    "www.booking.com",
    "www.zillow.com",
    "www.trulia.com",
    "www.realtor.com",
    "www.weather.com",
    "www.accuweather.com",
    "www.allrecipes.com",
    "www.foodnetwork.com",
    "www.epicurious.com",
    "www.bonappetit.com",
    "www.goodreads.com",
    "www.audible.com",
    "www.shopify.com",
    "www.walmart.com",
    "www.homedepot.com",
    "www.target.com",
    "www.lowes.com",
    "www.bestbuy.com",
    "www.costco.com",
    "www.kohls.com",
    "www.macys.com",
    "www.ikea.com",
    "www.wayfair.com",
    "www.shein.com",
    "www.zara.com",
    "www.hm.com",
    "www.pandora.com",
    "www.soundcloud.com",
    "www.twitch.tv",
    "www.roblox.com",
    "www.minecraft.net",
    "www.epicgames.com",
    "www.steampowered.com",
    "www.hulu.com",
    "www.disneyplus.com",
    "www.paramountplus.com",
    "www.peacocktv.com",
    "www.crunchyroll.com",
    "www.espnplus.com",
    "www.viu.com",
    "www.vimeo.com",
    "www.dailymotion.com",
    "www.quora.com",
    "www.medium.com",
    "www.dev.to",
    "www.gitlab.com",
    "www.bitbucket.org",
    "www.digitalocean.com",
    "www.heroku.com",
    "www.cloudflare.com",
    "www.wix.com",
    "www.squarespace.com",
    "www.wordpress.com",
    "www.weebly.com",
    "www.godaddy.com",
    "www.bluehost.com",
    "www.hostgator.com",
    "www.namecheap.com",
    "www.cloudflare.com"
]



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

def tester(proxy, github=False):
    p = {
        'http':f"{proxy}",
        'https':f"{proxy}"
    }
    site = random.randint(0,len(sites))
    site = sites[site]

    test_url = f"http://{site}"

    header = Headers(headers=True)

    h = header.generate()
    

    try:
        # Make a request through the SOCKS proxy
        response = requests.get(test_url, proxies=p, timeout=5, headers=h)
        response.raise_for_status()  # Check if the request was successful
        if github:
            "\033[34mThis is blue text\033[0m"
            print(f"\n\n\033[34mSOCKS proxy is working: {proxy} | {site}\033[0m\n\n")
        else:
            print(f"\n\nSOCKS proxy is working: {proxy} | {site}\n\n")
        return True
    except requests.exceptions.RequestException as e:
        if github:
            print(f"\033[34mSOCKS proxy failed: {proxy} | {site} | {h}\033[0m")
        else:
            print(f"SOCKS proxy failed: {proxy} | {site} | {h}")
        return False
    

def gitproxies4():
    url = 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/refs/heads/master/socks4.txt'
    r = requests.get(url)

    if r.status_code == 200:
        proxies = [f"socks4://{line.strip()}" for line in r.text.splitlines() if line.strip()]
        return proxies
    else:
        print(f"error {r.status_code}")