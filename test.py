# import psutil
# import time
# import fcntl

# def acquire_lock(file):
#     fcntl.flock(file.fileno(), fcntl.LOCK_EX)

# def release_lock(file):
#     fcntl.flock(file.fileno(), fcntl.LOCK_UN)

# def update_stats_file(container_name, cpu_percent, memory_percent, bytes_sent, bytes_received):
#     # Define the filename
#     filename = "profiling_engine.log"
#     data = {}
#     with open(filename, "r") as file:
#         for line in file:
#             parts = line.strip().split(":")
#             name = parts[0]
#             values = [float(x) if i > 0 else x for i, x in enumerate(parts[1:])]
#             data[name] = values
    
#     # Update the dictionary if container_name matches
#     if container_name in data:
#         data[container_name] = [cpu_percent, memory_percent, bytes_sent, bytes_received]
#         print(data[container_name])

#     # Write the updated content back to the file
#     with open(filename, "w") as file:
#         for container, values in data.items():
#             file.write(f"{container}:{':'.join(map(str, values))}\n")

# def get_next_container(algo):
#     global containers_ip
#     global containers_name
#     current_container = containers_ip[0]
#     if(algo=='round_robin'):
#         current_container = containers_ip[0]
#         containers_ip = containers_ip[1:] + [containers_ip[0]]
#         return current_container
#     if(algo=='cpu_load'):
#         # stats = _get_container_stats(containers_name)
#         best_ip = None
#         least_cpu = float('inf')
#         filename = "/logging/profiling_engine.log"
#         with open(filename, "r") as file:
#             acquire_lock(file)
#             for container_name in containers_name:
#                     for line in file:
#                         parts = line.strip().split(":")
#                         name = parts[0]
#                         if(name==container_name):
#                             cpu = float(parts[1])
#                             if(cpu<least_cpu):
#                                 best_ip = name_ip_mapper[container_name]
#                                 cpu = least_cpu
#                             break
#             release_lock(file)
#         return best_ip
#     return current_container

# if __name__=="__main__" :
#     print(get_next_container(algo))

import os

containers_name = ['container1', 'container2', 'container3']

filename = "profiling_engine.log"
for container_name in containers_name:
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(":")
            name = parts[0]
            print(parts)
            print(name)
            if(name==container_name):
                cpu = float(parts[1])
                print(cpu)
            print()