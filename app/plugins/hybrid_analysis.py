import requests

plugin_name = 'hybrid_analysis'
config = None

def check(query):
    api = config['api']
    secret = config['secret']
    url = 'https://www.hybrid-analysis.com/api/search?query={}&secret={}&apikey={}'.format(query, secret, api)
    req = requests.get(url).json()
    res = req
    res['found'] = True if res['response']['result'] != [] else False
    res['name'] = 'hybrid-analysis'
    return res

class Plugin:
    def __init__(self, conf):
        global config
        config = conf

    def register(self):
        return {plugin_name: {'check': check}}