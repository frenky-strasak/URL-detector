import json


# path = '/home/frenky/PycharmProjects/url_detector/URL-detector/data/urlscan_data/download.json'
path = '/home/frenky/Documents/Skola/Stratosphere_url_detector/final_data/data/output_data/normal/urlscan_json/0003/akairan.com.json'

with open(path) as f:
    json_data = json.load(f)
f.close()



"""
-> url, uuid, options about urlscan request
-> no features
"""
# print(json_data['task'])


"""
features:
1. type of server?
"""
# print(json_data['page'])


"""
1. ips of domain
2. contries
3. asns - Autonomous System Number 
4. all domains for our domain
5. all type of server
6. all? urls for our domain
7. linkdomains from our domain
8. certificates
9. hashes
"""
# print(json_data['lists'])



"""
1. confidence, confidenceTotal
"""
# print(json_data['meta'])



"""
1. resourceStats array
2. protocolStats
3. tlsStats
4. serverStats
5. domainStats
6. regDomainStats
7. ipStats
"""
# print(json_data['stats'])
# k = json_data['stats']['tlsStats'][0]['protocols']
# print(len(k))


"""

"""
# print(json_data['data'])


for request in json_data['data']['requests']:
    try:
        res = request['request']['redirectResponse']['headers']['Content-Length']
        print(res)
    except:
        pass
# asns_list_int = list(map(int, asns_list))