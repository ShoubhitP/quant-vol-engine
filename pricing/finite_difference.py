import numpy as np
from scipy.linalg import solve_banded

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

def implicit_fd_call(S, K, vol, r, T, N, M):

    s_max = 2 * S
    delta_S = s_max / N
    delta_t = T / M

    V = np.zeros((N + 1, M + 1))
    stock_grid = np.linspace(0, s_max, N + 1)
    V[:, M] = np.maximum(stock_grid - K, 0)

    for j in range(M - 1, -1, -1):
        V[0, j] = 0
        V[N, j] = s_max - K * np.exp(-r * (T - j * delta_t))
        
        i_vals = np.arange(1, N)
        Si = stock_grid[i_vals]
        
        # compute alpha, beta, gamma as vectors
        alpha = (delta_t / 2) * (
                ((vol**2 * Si**2) / delta_S**2)
                - ((r * Si) / delta_S)
            )
        beta = delta_t * ((vol**2 * Si**2) / delta_S**2 + r)
            
        gamma = (delta_t / 2) * (
                ((vol**2 * Si**2) / delta_S**2)
                + ((r * Si) / delta_S)
            )
        
        # build lower, main, upper diagonals
        lower = -1*alpha[1:]  #length N-2
        main = 1 + beta  # length N-1
        upper = -1*gamma[:-1]  # length N-2
        
        # build RHS
        rhs = V[i_vals, j+1].copy()
        rhs[0] += alpha[0] * V[0, j]
        rhs[-1] += gamma[-1] * V[N, j]
       
        ab = np.zeros((3, N-1))
        ab[0, 1:] = upper    # upper diagonal
        ab[1, :] = main      # main diagonal  
        ab[2, :-1] = lower   # lower diagonal
        V[1:N, j] = solve_banded((1,1), ab, rhs)

    return V[int(S / delta_S), 0]

def crank_nicolson_fd_call(S, K, vol, r, T, N, M):

    s_max = 2 * S
    delta_S = s_max / N
    delta_t = T / M

    V = np.zeros((N + 1, M + 1))
    stock_grid = np.linspace(0, s_max, N + 1)
    V[:, M] = np.maximum(stock_grid - K, 0)

    for j in range(M - 1, -1, -1):
        V[0, j] = 0
        V[N, j] = s_max - K * np.exp(-r * (T - j * delta_t))
        
        i_vals = np.arange(1, N)
        Si = stock_grid[i_vals]
        
        # compute alpha, beta, gamma as vectors
        alpha = (delta_t / 2) * (
                ((vol**2 * Si**2) / delta_S**2)
                - ((r * Si) / delta_S)
            )
        beta = delta_t * ((vol**2 * Si**2) / delta_S**2 + r)
            
        gamma = (delta_t / 2) * (
                ((vol**2 * Si**2) / delta_S**2)
                + ((r * Si) / delta_S)
            )
        
        # build lower, main, upper diagonals
        lower = (-1*alpha[1:]) / 2  #length N-2
        main = 1 + beta/2  # length N-1
        upper = (-1*gamma[:-1])/2  # length N-2
        
        # build RHS
        rhs = (alpha/2)*V[i_vals-1, j+1] + (1-beta/2)*V[i_vals, j+1] + (gamma/2)*V[i_vals+1, j+1]
        rhs[0] += (alpha[0]/2) * V[0, j]
        rhs[-1] += (gamma[-1]/2) * V[N, j]
       
        ab = np.zeros((3, N-1))
        ab[0, 1:] = upper    # upper diagonal
        ab[1, :] = main      # main diagonal  
        ab[2, :-1] = lower   # lower diagonal
        V[1:N, j] = solve_banded((1,1), ab, rhs)

    return V[int(S / delta_S), 0]

def american_put_cn(S, K, vol, r, T, N, M):

    s_max = 2 * S
    delta_S = s_max / N
    delta_t = T / M

    V = np.zeros((N + 1, M + 1))
    stock_grid = np.linspace(0, s_max, N + 1)
    V[:, M] = np.maximum(K-stock_grid, 0)

    for j in range(M - 1, -1, -1):
        V[0, j] = K * np.exp(-r * (T - j * delta_t))
        V[N, j] = 0

        i_vals = np.arange(1, N)
        Si = stock_grid[i_vals]
        
        # compute alpha, beta, gamma as vectors
        alpha = (delta_t / 2) * (
                ((vol**2 * Si**2) / delta_S**2)
                - ((r * Si) / delta_S)
            )
        beta = delta_t * ((vol**2 * Si**2) / delta_S**2 + r)
            
        gamma = (delta_t / 2) * (
                ((vol**2 * Si**2) / delta_S**2)
                + ((r * Si) / delta_S)
            )
        
        # build lower, main, upper diagonals
        lower = (-1*alpha[1:]) / 2  #length N-2
        main = 1 + beta/2  # length N-1
        upper = (-1*gamma[:-1])/2  # length N-2

        # build RHS
        rhs = (alpha/2)*V[i_vals-1, j+1] + (1-beta/2)*V[i_vals, j+1] + (gamma/2)*V[i_vals+1, j+1]
        rhs[0] += (alpha[0]/2) * V[0, j]
        rhs[-1] += (gamma[-1]/2) * V[N, j]
       
        ab = np.zeros((3, N-1))
        ab[0, 1:] = upper    # upper diagonal
        ab[1, :] = main      # main diagonal  
        ab[2, :-1] = lower   # lower diagonal
        V[1:N, j] = solve_banded((1,1), ab, rhs)
        V[i_vals, j] = np.maximum(V[i_vals, j], K - Si)     

    return V[int(S / delta_S), 0]
    

#if __name__ == "__main__":

    #print("Explicit Finite Difference Call Price:", explicit_fd_call(100, 100, 0.2, 0.05, 1, 100, 1000))
    #print("Explicit Finite Difference Call Price:", explicit_fd_call(100, 100, 0.2, 0.05, 1, 200, 2000))
    #print("Implicit Finite Difference Call Price:", implicit_fd_call(100, 100, 0.2, 0.05, 1, 100, 1000))
    #print("Crank-Nicolson Finite Difference Call Price:", crank_nicolson_fd_call(100, 100, 0.2, 0.05, 1, 100, 1000))
    #print("Crank-Nicolson Finite Difference Call Price (American Option):", american_put_cn(100, 100, 0.2, 0.05, 1, 100, 1000))


#main()

