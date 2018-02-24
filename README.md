metasearch
===========

Purpose: stop searching for sample hashes on 10 different sites.
This is a simple Python3 Flask application running on port 5000 interacting with various platforms (TBC) and caching the results in a Redis database for faster responses. 

### Installation

Git clone the repository: 

```bash
$ git clone https://github.com/PaulSec/metasearch.git
$ cd metasearch
```


Add your API tokens (and Redis parameters) for the specific plugins in the app/config-sample.json file: 

```json
{
    "hybrid_analysis": {
        "api": "XXXXXXXXXXXXXXXXXX",
        "secret": "XXXXXXXXXXXXXXXXXX"
    },
    "malshare": {
        "api": "XXXXXXXXXXXXXXXXXX"
    },
    "redis_host": "redis",
    "redis_port": 6379
}
```


Finally, rename it from ```config-sample.json``` to ```config.json```

### Quickstart (with docker-compose)

Then, use docker-compose in the metasearch directory: 

```bash
$ docker-compose up
Recreating metasearch_web_1 ...
Recreating metasearch_web_1
Starting metasearch_redis_1 ...
Recreating metasearch_web_1 ... done
Attaching to metasearch_redis_1, metasearch_web_1
redis_1  | 1:C 23 Feb 20:12:16.838 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis_1  | 1:C 23 Feb 20:12:16.840 # Redis version=4.0.8, bits=64, commit=00000000, modified=0, pid=1, just started
redis_1  | 1:C 23 Feb 20:12:16.840 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis_1  | 1:M 23 Feb 20:12:16.845 * Running mode=standalone, port=6379.
redis_1  | 1:M 23 Feb 20:12:16.845 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
redis_1  | 1:M 23 Feb 20:12:16.845 # Server initialized
redis_1  | 1:M 23 Feb 20:12:16.845 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
redis_1  | 1:M 23 Feb 20:12:16.848 * DB loaded from disk: 0.003 seconds
redis_1  | 1:M 23 Feb 20:12:16.848 * Ready to accept connections
web_1    |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
web_1    |  * Restarting with stat
web_1    |  * Debugger is active!
web_1    |  * Debugger PIN: 216-090-375
web_1    | 172.20.0.1 - - [23/Feb/2018 20:12:45] "GET /plugins HTTP/1.1" 200 -
```

The service is accessible at ```http://0.0.0.0:5000```. You can check by typing:

```bash
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                    PORTS                    NAMES
3ed6edac232d        metasearch_web      "python main.py"         About an hour ago   Up About an hour          0.0.0.0:5000->5000/tcp   metasearch_web_1
6bddda639254        redis:alpine        "docker-entrypoint..."   2 hours ago         Up About an hour          6379/tcp                 metasearch_redis_1
```

### Interacting with the API

Those are the different API endpoint accessible:

HTTP Method | URI | HTTP Method
--- | --- | ---
|GET | /plugins | Lists all the plugins loaded within the application |
|GET | /hybrid_analysis/hash | Will check the hash provided on [Hybrid-analysis](https://www.hybrid-analysis.com/) |
|GET | /virustotal/hash | Will check the hash provided on [VirusTotal](https://www.virustotal.com/) |
|GET | /malshare/hash | Will check the hash provided on [MalShare](http://malshare.com/) |
|GET | /virusbay/hash | Will check the hash provided on [VirusBay](https://beta.virusbay.io) |
|GET | /search/hash | Will check on all the platforms listed above |

### Examples: 

##### Retrieving all the plugins

```bash
$ curl http://0.0.0.0:5000/plugins -s | jq .
[
  "virustotal",
  "malshare",
  "virusbay",
  "hybrid_analysis"
]
```

#### Looking up ```d84769d63aa6b8718ab4bd86e27e26a4``` on MalShare.

```bash
$ curl http://0.0.0.0:5000/malshare/d84769d63aa6b8718ab4bd86e27e26a4 -s | jq .
{
  "found": true,
  "data": {
    "SHA1": "78cac2c75b0fe9e7d3819341a451dabcad4d7678",
    "MD5": "d84769d63aa6b8718ab4bd86e27e26a4",
    "F_TYPE": "PE32",
    "SHA256": "c2c855b71cc8b1c1c731f4cadab8a24db4cd8b66f8583cb9640c35d296baf6b0",
    "SOURCES": [
      "http://109.234.36.233/bot/Miner/bin/Release/LoaderBot.exe"
    ],
    "SSDEEP": "384:fKxvDuPNItH19GTXjdh8duujYcV6AUwJFZb:f44atV9AhsfYcV6Dw9b"
  },
  "name": "malshare"
}
```


##### Looking up ```2dd395cbd297e8b40a4b64b3bb21e655``` on all the platforms. 

```bash
$ curl http://0.0.0.0:5000/search/2dd395cbd297e8b40a4b64b3bb21e655 -s | jq . | more
[
  {
    "links": {
      "self": "https://www.virustotal.com/ui/search?query=2dd395cbd297e8b40a4b64b3bb21e655&relationships[url]=network_location%2Clast_serving_ip_address&relationships[comment]=author%2Citem"
    },
    "data": [
      {
        "attributes": {
          "names": [
            "482931ee6c24d9ead3e4024b62106286992cfa3d",
            "bash"
          ],
          "elf_info": {
            "imports": [
              [
                "__deregister_frame_info",
                "NOTYPE"
              ],
              [
                "__pthread_initialize_minimal",
                "NOTYPE"
              ],

[..redacted..]

        "type": "file"
      }
    ],
    "found": true,
    "name": "virustotal"
  },
  {
    "found": false,
    "data": [],
    "name": "malshare"
  },
  {
    "search": [
      {
        "tags": [
          {
            "__v": 0,
            "isHash": false,
            "_id": "5a3b6199697fdd3b4ded78f6",
            "lowerCaseName": "elf",
            "name": "elf"
          },
          {
            "__v": 0,
            "isHash": false,
            "_id": "5a3b6199697fdd3b4ded78f7",
            "lowerCaseName": "linux",
            "name": "linux"
[..redacted..]
```

License
========

This project has been released under MIT License.
Contributions are more than welcome. Ping me on Twitter [@PaulWebSec](https://twitter.com/PaulWebSec) if you want some help for that.