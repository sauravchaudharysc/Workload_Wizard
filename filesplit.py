def parse_file(filename):
    data = {}
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(":")
            container_name = parts[0]
            values = [float(x) if i > 0 else x for i, x in enumerate(parts[1:])]
            data[container_name] = values
    return data

filename = "profiling_engine.log"  # Update with your file name
container_data = parse_file(filename)
print(container_data)
