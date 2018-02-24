#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, json, jsonify
import requests, json, sys, redis, os

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello !"

# Endpoint to list all the plugins
@app.route('/plugins')
def retrieve_plugins():
    plugins_names = list(plugins)
    print(plugins_names)
    response = app.response_class(
        response=json.dumps(plugins_names),
        status=200,
        mimetype='application/json'
    )
    return response    

# Search with all the plugins
@app.route('/search/<string:query>')
def search(query):
    # Iterate over all the plugins
    result = []
    for plugin in plugins:
        # checking in the Redis if the entry is already there
        test_redis = cache.get('{}_{}'.format(plugin, query))
        if test_redis:
            test_redis = test_redis.decode('utf-8')
            tmp_result = json.loads(test_redis)
        else:
            tmp_result = plugins[plugin]['check'](query)
            cache.set('{}_{}'.format(plugin, query), json.dumps(tmp_result))
        result.append(tmp_result)

    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/<string:provider>/<string:query>')
def search_provider(provider, query):
    # Checking if the provider is listed
    if provider not in list(plugins):
        response = app.response_class(
            response=None,
            status=404
        )
        return response

    # checking in the Redis if the entry is already there
    test_redis = cache.get('{}_{}'.format(provider, query))
    if test_redis:
        test_redis = test_redis.decode('utf-8')
        result = json.loads(test_redis)
        response = app.response_class(
            response=json.dumps(result),
            status=200 if result['found'] else 404,
            mimetype='application/json'
        )
        return response

    # If not, it fetches it
    result = plugins[provider]['check'](query)
    cache.set('{}_{}'.format(provider, query), json.dumps(result))
    response = app.response_class(
        response=json.dumps(result),
        status=200 if result['found'] else 404,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':

    path = "plugins/"
    plugins = {}

    # Retrieve the configuration
    with open('config.json') as f:
        config = json.loads(f.read())

    # Load plugins
    sys.path.insert(0, path)
    for f in os.listdir(path):
        fname, ext = os.path.splitext(f)
        if ext == '.py':
            try:
                mod = __import__(fname)
                plugin_config = None
                if fname in config:
                    plugin_config = config[fname]
                plugin = mod.Plugin(plugin_config)
                tmp_res = plugin.register()
                plugin_name = list(tmp_res)[0]
                plugin_functions = tmp_res[plugin_name]
                plugins[plugin_name] = plugin_functions
                # print(plugins)
            except Exception as err:
                print('[!] Problem loading plugin with file {}'.format(fname))
                print(err)

    cache = redis.Redis(host=config['redis_host'], port=config['redis_port'])
    print(cache)

    app.run(host='0.0.0.0', debug=True)

