from flask import Flask,jsonify, request
import requests
import sys
import socket
import docker
import json
import fcntl
# Update this variable as per your setup
# COUNTER_SERVICE_URL = 'http://192.168.2.2:8080' if len(sys.argv) == 1 else sys.argv[1]

app = Flask(__name__)
client = docker.from_env()
containers_ip = []
containers_name = ['container1', 'container2', 'container3', 'container4', 'container5','container6', 'container7', 'container8', 'container9', 'container10', 'container11', 'container12', 'container13', 'container14', 'container15']#,'container16', 'container17', 'container18', 'container19', 'container20']
name_ip_mapper = {}

def acquire_lock(file):
    fcntl.flock(file.fileno(), fcntl.LOCK_EX)

def release_lock(file):
    fcntl.flock(file.fileno(), fcntl.LOCK_UN)

def _get_container_stats(containers_name):
    global containers_ip
    if not containers_ip:
        # Handle the case when containers_ip is empty
        for container_name in containers_name:
            containers_ip.append(socket.gethostbyname(container_name.strip()))
            name_ip_mapper[container_name] = containers_ip[-1]

    all_stats = {}
    for container_name in containers_name:        
        container = client.containers.get(container_name)
        stats = container.stats(stream=False)
        cpu_stats = stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage'] * 100
        memory_stats = stats['memory_stats']['usage']/ (1024 * 1024)
        network_stats = stats['networks']
        container_stats = {
                'ip': name_ip_mapper[container_name],
                'memory': memory_stats,
                'cpu': cpu_stats,
                'network': network_stats
            }
        all_stats[container_name] = container_stats
    return all_stats


@app.route('/all_stats')
def get_container_stats():
    # containers_name = ['container1', 'container2', 'container3']
    return jsonify(_get_container_stats(container_name))

def get_container_ip(container_name):
    try:
        container = client.containers.get(container_name)
        networks = container.attrs['NetworkSettings']['Networks']
        # Assuming the container is connected to only one network
        network_name = list(networks.keys())[0]
        return networks[network_name]['IPAddress']
    except docker.errors.NotFound:
        print(f"Container '{container_name}' not found.")
    except KeyError:
        print(f"Could not retrieve IP address for container '{container_name}'.")


def get_next_container(algo):
    global containers_ip
    global containers_name
    current_container = containers_ip[0]
    if(algo=='round_robin'):
        current_container = containers_ip[0]
        containers_ip = containers_ip[1:] + [containers_ip[0]]
        return current_container
    if(algo=='cpu_load'):
        # stats = _get_container_stats(containers_name)
        best_ip = None
        least_cpu = float('inf')
        filename = "/logging/profiling_engine.log"
        for container_name in containers_name:
            with open(filename, "r") as file:    
                acquire_lock(file)
                for line in file:
                    parts = line.strip().split(":")
                    name = parts[0]
                    if(name==container_name):
                        cpu = float(parts[1])
                        if(cpu<least_cpu):
                            best_ip = name_ip_mapper[container_name]
                            least_cpu = cpu
                release_lock(file)
        return best_ip
    return current_container



@app.route('/')
def hello_world():
    global containers_ip
    global containers_name
    if not containers_ip:
        # Handle the case when containers_ip is empty
        # containers_name = ['container1', 'container2', 'container3']
        for container_name in containers_name:
            containers_ip.append(socket.gethostbyname(container_name.strip()))
            name_ip_mapper[container_name] = containers_ip[-1]
    current_container = get_next_container('cpu_load')
    duration_seconds = request.args.get('duration_seconds')
    memory_load = request.args.get('memory_load')
    load_type = request.args.get('type_type')
    params = {
        'duration_seconds': duration_seconds,
        'memory_load': memory_load,
        'load_type': load_type
    }
    res = requests.get("http://"+current_container + ':5000/', params=params)
    return 'Hello CS695 Explorers! You have sent request to this container '+res.text


if __name__ == '__main__':
    
    for container_name in containers_name:
        containers_ip.append(socket.gethostbyname(container_name.strip()))
        name_ip_mapper[container_name] = containers_ip[-1]
    app.run(host='0.0.0.0', port=8080, threaded = True)

# from flask import Flask, jsonify, request
# import requests
# import socket
# import docker
# import json
# from threading import Thread, Lock
# import time
# import logging


# app = Flask(__name__)
# log = logging.getLogger('werkzeug')
# log.disabled = True
# client = docker.from_env()
# containers_ip = []
# containers_name = ['container1', 'container2', 'container3']
# name_ip_mapper = {}
# container_stats_cache = {}
# cache_lock = Lock()

# def _fetch_container_stats(containers_name):
#     global container_stats_cache
#     while True:
#         try:
#             all_stats = {}
#             for container_name in containers_name:
#                 try:
#                     container = client.containers.get(container_name)
#                     stats = container.stats(stream=False)
#                     cpu_stats = stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage'] * 100
#                     memory_stats = stats['memory_stats']['usage'] / (1024 * 1024)
#                     network_stats = stats['networks']
#                     container_stats = {
#                         'ip': name_ip_mapper[container_name],
#                         'memory': memory_stats,
#                         'cpu': cpu_stats,
#                         'network': network_stats
#                     }
#                     all_stats[container_name] = container_stats
#                 except Exception as e:
#                     print(f"Error occurred while fetching stats for container '{container_name}': {str(e)}")

#             with cache_lock:
#                 container_stats_cache = all_stats
#         except Exception as e:
#             print(f"Error occurred while fetching container stats: {str(e)}")
#         time.sleep(2)  # Fetch stats every 60 seconds

# fetch_stats_thread = Thread(target=_fetch_container_stats, args=(containers_name,))
# fetch_stats_thread.daemon = True
# fetch_stats_thread.start()

# @app.route('/all_stats')
# def get_container_stats():
#     with cache_lock:
#         return jsonify(container_stats_cache)

# def get_container_ip(container_name):
#     try:
#         container = client.containers.get(container_name)
#         networks = container.attrs['NetworkSettings']['Networks']
#         network_name = list(networks.keys())[0]
#         return networks[network_name]['IPAddress']
#     except docker.errors.NotFound:
#         print(f"Container '{container_name}' not found.")
#     except KeyError:
#         print(f"Could not retrieve IP address for container '{container_name}'.")

# def get_next_container(algo):
#     global containers_ip
#     global containers_name
#     current_container = containers_ip[0]
#     if algo == 'round_robin':
#         current_container = containers_ip[0]
#         containers_ip = containers_ip[1:] + [containers_ip[0]]
#         return current_container
#     if algo == 'cpu_load':
#         with cache_lock:
#             stats = container_stats_cache
#         print("stats:", stats)
#         best_ip = None
#         least_cpu = float('inf')
#         for container_name, value in stats.items():
#             if value['cpu'] < least_cpu:
#                 best_ip = value['ip']
#                 least_cpu = value['cpu']
#         return best_ip
#     return current_container

# @app.route('/')
# def hello_world():
#     global containers_ip
#     global containers_name
#     if not containers_ip:
#         for container_name in containers_name:
#             containers_ip.append(socket.gethostbyname(container_name.strip()))
#             name_ip_mapper[container_name] = containers_ip[-1]
#     current_container = get_next_container('cpu_load')
#     duration_seconds = request.args.get('duration_seconds')
#     memory_load = request.args.get('memory_load')
#     load_type = request.args.get('type_type')
#     params = {
#         'duration_seconds': duration_seconds,
#         'memory_load': memory_load,
#         'load_type': load_type
#     }
#     res = requests.get("http://" + current_container + ':5000/', params=params)
#     return 'Hello CS695 Explorers! You have sent request to this container ' + res.text

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)

