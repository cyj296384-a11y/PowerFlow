import json

def load_ieee14(path="data/ieee14.json"):
    with open(path, "r") as f:
        data = json.load(f)
    return data


def get_branches(data):
    return data["branch"]


def get_bus_count(data):
    return len(data["bus"])
def classify_buses(data):
    slack = []
    pv = []
    pq = []

    for bus in data["bus"]:
        if bus["type"] == "slack":
            slack.append(bus["id"])
        elif bus["type"] == "PV":
            pv.append(bus["id"])
        else:
            pq.append(bus["id"])

    return slack, pv, pq