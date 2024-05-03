import requests
import simple_colors
import time

# Define the base URL
base_url = 'http://192.168.64.5:8000'

def throughput_testing(num_requests, duration_seconds):
    start_time = time.time()
    sleep_time=0
    for _ in range(num_requests):
        # Generating load
        # Define the parameters as a dictionary
        params = {
            'duration_seconds': duration_seconds,
            'memory_load': 0,
            'load_type': 'cpu'
        }
        response = requests.get(base_url, params=params)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Process the response
            print("Request successful:", response.text)
        else:
            print(f"Request failed with status code {response.status_code}")
        time.sleep(1)
        sleep_time+=1
    end_time = time.time()
    elapsed_time = end_time - start_time - sleep_time
    throughput = num_requests / elapsed_time
    print("Throughput:", throughput, "requests per second")

def get_stats():
    # Getting the stats
    response = requests.get(base_url+'/all_stats')
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Process the response
        for container, value in response.json().items():
            print("**** " + container +"("+value['ip']+")" " ****")
            print("Memory: ", value['memory'], "bytes")
            print("CPU: ", value['cpu'], "units")
            print("Network:")
            print("Bytes Received: ", value['network']['eth0']['rx_bytes'], "bytes")
            print("Bytes Sent: ", value['network']['eth0']['tx_bytes'], "bytes")
            print("Packets Received: ", value['network']['eth0']['rx_packets'])
            print("Packets Sent: ", value['network']['eth0']['tx_packets'])
            print()
            print()
    else:
        print(f"Request failed with status code {response.status_code}")

def send_load(duration,type):
    params = {
        'duration_seconds': duration,
        'memory_load': 0,
        'load_type': type
    }
    response = requests.get(base_url, params=params)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Process the response
        print(simple_colors.yellow(response.text))
    else:
        print(f"Request failed with status code {response.status_code}")

if __name__ == "__main__":
    throughput_testing(3, 30)
