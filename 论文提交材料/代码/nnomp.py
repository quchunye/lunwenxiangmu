#!/vol01/homes/hy87731/bin/python3
import numpy as np
from scipy.optimize import nnls
import time
import sys

def randomized_omp(A, b, k):
    best_residual = 1
    while best_residual > 1E-5:
        support = np.random.choice(A.shape[1], size=1, replace=False)
        residual = b.copy()
        for i in range(k-1):
            correlations = A.T @ residual
            correlations[list(support)] = 0
            max_indices = np.where(correlations == np.max(correlations))[0]
            new_index = np.random.choice(max_indices)
            support = np.append(support, new_index)
            A_support = A[:, support]
            x_support, _ = nnls(A_support, b)
            residual = b - A_support @ x_support
        best_residual = np.linalg.norm(residual)
    best_x = np.zeros(A.shape[1])
    best_x[support] = x_support
    return best_x


start_time = time.time()

k = int(sys.argv[1])

A = np.loadtxt('corr')
A = np.transpose(A)
n = A.shape[1]
A = np.vstack((A, np.ones(n)))
m = A.shape[0]
b = np.zeros(m)
b[-1] = 1

w = randomized_omp(A, b, k)
d = abs(A @ w - b)
print(d)
c = np.nonzero(w)[0]
print(c+1)
print(w[c])

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} sec")
