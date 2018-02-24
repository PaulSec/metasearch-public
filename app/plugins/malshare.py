import requests

plugin_name = 'malshare'
config = None

def check(query):
    API_KEY = config['api']
    url ='https://malshare.com/api.php?api_key={}&action=details&hash={}'.format(API_KEY, query)
    print(url)
    req = requests.get(url)
    res = {}
    res['found'] = True if b'Sample not found by hash' not in req.content else False
    res['data'] = req.json() if res['found'] else []
    res['name'] = 'malshare'
    return res

class Plugin:
    def __init__(self, conf):
        global config
        config = conf

    def register(self):
        return {plugin_name: {'check': check}}