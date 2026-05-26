import numpy as np

def explicit_fd_call(S, K, vol, r, T, N, M):
    s_max = 2 * S
    delta_S = s_max / N
    delta_t = T / M

    V = np.zeros((N + 1, M + 1))
    stock_grid = np.linspace(0, s_max, N + 1)

    V[:, M] = np.maximum(stock_grid - K, 0)

    for j in range(M - 1, -1, -1):
        V[0, j] = 0
        V[N, j] = s_max - K * np.exp(-r * (T - j * delta_t))

        for i in range(1, N):
            alpha = (delta_t / 2) * (
                ((vol**2 * stock_grid[i]**2) / delta_S**2)
                - ((r * stock_grid[i]) / delta_S)
            )

            beta = 1 - delta_t * (
                ((vol**2 * stock_grid[i]**2) / delta_S**2) + r
            )

            gamma = (delta_t / 2) * (
                ((vol**2 * stock_grid[i]**2) / delta_S**2)
                + ((r * stock_grid[i]) / delta_S)
            )

            V[i, j] = (
                alpha * V[i - 1, j + 1]
                + beta * V[i, j + 1]
                + gamma * V[i + 1, j + 1]
            )

    return V[int(S / delta_S), 0]

if __name__ == "__main__":

    print("Explicit Finite Difference Call Price:", explicit_fd_call(100, 100, 0.2, 0.05, 1, 100, 1000))
    print("Explicit Finite Difference Call Price:", explicit_fd_call(100, 100, 0.2, 0.05, 1, 200, 2000))


