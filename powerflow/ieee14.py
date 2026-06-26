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
import numpy as np

def get_power_spec(data):
    import numpy as np

    nb = len(data["bus"])

    P_spec = np.zeros(nb)
    Q_spec = np.zeros(nb)

    # ⚡ 自动适配：只填存在的节点
    loads = [
        (0.0, 0.0),
        (0.21, 0.127),
        (0.94, 0.19),
    ]

    for i in range(nb):
        if i < len(loads):
            P_spec[i], Q_spec[i] = loads[i]

    return P_spec, Q_spec
def get_bus_types(data):
    """
    自动生成节点类型
    默认规则：
    - 1号节点 = Slack
    - 其余 = PQ（先简化）
    """

    nb = len(data["bus"])

    bus_types = []

    for bus in data["bus"]:
        if bus["id"] == 1:
            bus_types.append("Slack")
        else:
            bus_types.append("PQ")

    return bus_types