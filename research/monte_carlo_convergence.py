import numpy as np
import matplotlib.pyplot as plt

from pricing.black_scholes import black_scholes_call
from pricing.monte_carlo import monte_carlo_call

S, K, vol, r, T = 100, 100, 0.2, 0.05, 1

bs_price = black_scholes_call(S, K, vol, r, T)

simulation_counts = [100, 1000, 10000, 100000, 1000000]

prices = []
avg_errors = []
avg_ci_widths = []

trials = 20

for n in simulation_counts:
    trial_errors = []
    trial_ci_widths = []

    for _ in range(trials):
        price, lower, upper = monte_carlo_call(S, K, vol, r, T, n)
        trial_errors.append(abs(price - bs_price))
        trial_ci_widths.append(upper - lower)

    avg_error = np.mean(trial_errors)
    avg_ci_width = np.mean(trial_ci_widths)

    avg_errors.append(avg_error)
    avg_ci_widths.append(avg_ci_width)

    print(
        f"N={n:<8} "
        f"BS={bs_price:.4f} "
        f"Avg Error={avg_error:.4f} "
        f"Avg CI Width={avg_ci_width:.4f}"
    )
plt.figure()
plt.plot(simulation_counts, avg_errors, marker="o")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Number of Simulations")
plt.ylabel("Absolute Error")
plt.title("Monte Carlo Convergence to Black-Scholes")
plt.grid(True)
plt.savefig("research/mc_error_convergence.png", dpi=300, bbox_inches="tight")
plt.show()

plt.figure()
plt.plot(simulation_counts, avg_ci_widths, marker="o")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Number of Simulations")
plt.ylabel("95% Confidence Interval Width")
plt.title("Monte Carlo Confidence Interval Shrinkage")
plt.grid(True)
plt.savefig("research/mc_ci_shrinkage.png", dpi=300, bbox_inches="tight")
plt.show()