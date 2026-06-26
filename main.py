from powerflow.ieee14 import (
    load_ieee14,
    get_branches,
    get_bus_count,
    get_power_spec,
    get_bus_types
)

from powerflow.ybus import calc_ybus
from powerflow.solver import nr_powerflow
import numpy as np


print("PowerFlow 启动 🚀")

# =========================
# 1. 读取数据
# =========================
data = load_ieee14()

branches = get_branches(data)
nb = get_bus_count(data)

# =========================
# 2. 构建 Ybus
# =========================
Ybus = calc_ybus(branches, nb)

print("\nYbus矩阵：")
print(Ybus)

# =========================
# 3. P/Q负荷
# =========================
P_spec, Q_spec = get_power_spec(data)

P_spec = np.array(P_spec)
Q_spec = np.array(Q_spec)

print("\nP_spec:", P_spec)
print("Q_spec:", Q_spec)

# =========================
# 4. 节点类型（关键修复点）
# =========================
bus_types = get_bus_types(data)

print("\nbus_types:", bus_types)

# =========================
# 5. NR潮流计算
# =========================
V = nr_powerflow(Ybus, P_spec, Q_spec, bus_types)

# =========================
# 6. 输出结果
# =========================
print("\n⚡ 最终电压结果：")
print(V)