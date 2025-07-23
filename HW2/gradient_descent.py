#Cody Hathcoat      CS441       July 22nd, 2025

import numpy as np

#Function for analysis
def f(x, y):
    return 5 * x**2 + 40 * x + y**2 -12 * y + 127

#Return both partial derivatives.
def grad_f(x, y):
    df_dx = 10 * x + 40
    df_dy = 2 * y - 12
    return np.array([df_dx, df_dy])

def gradient_descent(eta, steps=500):
    best_val = float('inf')
    best_point = None

    for trial in range(10):
        x, y = np.random.uniform(-10, 10, size=2)

        for _ in range(steps):
            grad = grad_f(x, y)
            x -= eta * grad[0]
            y -= eta * grad[1]

        val = f(x, y)
        if val < best_val:
            best_val = val
            best_point = (round(float(x), 6), round(float(y), 6))
    return best_val, best_point

#The experiments
etas = [0.1, 0.01, 0.001]
results = {}

for eta in etas:
    val, point = gradient_descent(eta)
    results[eta] = (val, point)

for eta, (val, point) in results.items():
    print(f"η = {eta} ---> Best Value: {val:.6f} at point (x, y) = {point}")