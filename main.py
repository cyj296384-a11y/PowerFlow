from powerflow.ieee14 import load_ieee14, get_branches, get_bus_count
from powerflow.ybus import calc_ybus


def main():
    print("PowerFlow 启动 🚀")

    data = load_ieee14()
    branches = get_branches(data)
    nb = get_bus_count(data)

    Y = calc_ybus(branches, nb)

    print("\nYbus矩阵：")
    print(Y)


if __name__ == "__main__":
    main()
from powerflow.ieee14 import load_ieee14, classify_buses

def main():
    data = load_ieee14()

    slack, pv, pq = classify_buses(data)

    print("Slack节点:", slack)
    print("PV节点:", pv)
    print("PQ节点:", pq)

if __name__ == "__main__":
    main()    