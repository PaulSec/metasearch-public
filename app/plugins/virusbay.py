import requests

plugin_name = 'virusbay'

def check(query):
    url = 'https://beta.virusbay.io/sample/search?q={}'.format(query)
    req = requests.get(url).json()
    res = req
    res['found'] = True if req['search'] != [] else False
    res['name'] = 'virustotal'
    return res

class Plugin:
    def __init__(self, conf):
        pass

    def register(self):
        return {plugin_name: {'check': check}}