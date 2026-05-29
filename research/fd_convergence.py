import matplotlib.pyplot as plt

from pricing.black_scholes import black_scholes_call
from pricing.finite_difference import (
    explicit_fd_call,
    implicit_fd_call,
    crank_nicolson_fd_call,
)

S, K, vol, r, T = 100, 100, 0.2, 0.05, 1
bs_price = black_scholes_call(S, K, vol, r, T)

grid_sizes = [25, 50, 100, 200]

explicit_errors = []
implicit_errors = []
cn_errors = []

for N in grid_sizes:
    M_explicit = 5 * N * N
    M_implicit_cn = 10 * N

    explicit_price = explicit_fd_call(S, K, vol, r, T, N, M_explicit)
    implicit_price = implicit_fd_call(S, K, vol, r, T, N, M_implicit_cn)
    cn_price = crank_nicolson_fd_call(S, K, vol, r, T, N, M_implicit_cn)

    explicit_error = abs(explicit_price - bs_price)
    implicit_error = abs(implicit_price - bs_price)
    cn_error = abs(cn_price - bs_price)

    explicit_errors.append(explicit_error)
    implicit_errors.append(implicit_error)
    cn_errors.append(cn_error)

    print(
        f"N={N:<4} "
        f"M_exp={M_explicit:<7} "
        f"M_imp_cn={M_implicit_cn:<5} "
        f"BS={bs_price:.4f} | "
        f"Explicit={explicit_price:.4f} Error={explicit_error:.4f} | "
        f"Implicit={implicit_price:.4f} Error={implicit_error:.4f} | "
        f"CN={cn_price:.4f} Error={cn_error:.4f}"
    )

plt.figure()
plt.plot(grid_sizes, explicit_errors, marker="o", label="Explicit")
plt.plot(grid_sizes, implicit_errors, marker="o", label="Implicit")
plt.plot(grid_sizes, cn_errors, marker="o", label="Crank-Nicolson")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Stock Grid Size N")
plt.ylabel("Absolute Error vs Black-Scholes")
plt.title("Finite Difference Convergence")
plt.grid(True)
plt.legend()
plt.savefig("research/fd_convergence.png", dpi=300, bbox_inches="tight")
plt.show()