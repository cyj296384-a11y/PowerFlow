import numpy as np


# =========================================================
# 1. 复功率计算 S = V * I*
# =========================================================
def power(V, Ybus):
    I = Ybus @ V
    S = V * np.conj(I)
    return S.real, S.imag


# =========================================================
# 2. θ + |V| → 复数电压
# =========================================================
def polar_to_complex(theta, Vmag):
    return Vmag * np.exp(1j * theta)


# =========================================================
# 3. 仅PQ节点索引提取工具
# =========================================================
def get_pq_indices(bus_types):
    """
    bus_types: list like ["Slack","PQ","PQ",...]
    """
    return [i for i, t in enumerate(bus_types) if t == "PQ"]


# =========================================================
# 4. 数值Jacobian（稳定版NR核心）
# =========================================================
def numerical_jacobian(theta, Vmag, Ybus, pq_idx):
    nb = len(theta)
    n = len(pq_idx)

    size = 2 * n
    J = np.zeros((size, size))

    eps = 1e-6

    def calc(th, vm):
        V = vm * np.exp(1j * th)
        I = Ybus @ V
        S = V * np.conj(I)
        return S.real, S.imag

    baseP, baseQ = calc(theta, Vmag)

    for k, i in enumerate(pq_idx):

        # -------- θ扰动 --------
        th = theta.copy()
        th[i] += eps
        P1, Q1 = calc(th, Vmag)

        J[:n, k] = (P1[pq_idx] - baseP[pq_idx]) / eps
        J[n:, k] = (Q1[pq_idx] - baseQ[pq_idx]) / eps

        # -------- V扰动 --------
        vm = Vmag.copy()
        vm[i] += eps
        P2, Q2 = calc(theta, vm)

        J[:n, k+n] = (P2[pq_idx] - baseP[pq_idx]) / eps
        J[n:, k+n] = (Q2[pq_idx] - baseQ[pq_idx]) / eps

    return J


# =========================================================
# 5. NR潮流主函数（标准结构）
# =========================================================
def nr_powerflow(Ybus, P_spec, Q_spec, bus_types, max_iter=15, tol=1e-6):

    nb = len(P_spec)

    # 初始值
    theta = np.zeros(nb)
    Vmag = np.ones(nb)

    # PQ节点
    pq_idx = get_pq_indices(bus_types)

    print("\n⚡ NR潮流计算开始\n")

    for it in range(max_iter):

        V = polar_to_complex(theta, Vmag)

        P, Q = power(V, Ybus)

        # 不平衡
        dP = P_spec - P
        dQ = Q_spec - Q

        mismatch = np.hstack([dP[pq_idx], dQ[pq_idx]])

        error = np.max(np.abs(mismatch))
        print(f"迭代 {it+1}: 最大误差 = {error:.6e}")

        if error < tol:
            print("\n✔ 收敛成功（NR结束）\n")
            break

        # Jacobian
        J = numerical_jacobian(theta, Vmag, Ybus, pq_idx)

        # 解线性方程
        try:
            dx = np.linalg.solve(J, mismatch)
        except np.linalg.LinAlgError:
            print("❌ Jacobian奇异（检查Ybus或PQ节点）")
            break

        n = len(pq_idx)

        dtheta = dx[:n]
        dV = dx[n:]

        # 更新（阻尼，防发散）
        alpha = 0.3

        theta[pq_idx] += alpha * dtheta
        Vmag[pq_idx] += alpha * dV

    return polar_to_complex(theta, Vmag)