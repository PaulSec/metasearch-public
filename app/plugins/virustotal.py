import requests

plugin_name = 'virustotal'

def check(query):
    url = 'https://www.virustotal.com/ui/search?query={}&relationships[url]=network_location%2Clast_serving_ip_address&relationships[comment]=author%2Citem'.format(query)
    req = requests.get(url).json()
    res = req
    res['found'] = True if len(req['data']) > 0 and 'attributes' in req['data'][0] else False
    res['name'] = 'virustotal'
    return res

class Plugin:
    def __init__(self, conf):
        pass

    def register(self):
        return {plugin_name: {'check': check}}