import numpy as np

# --- 1. Root Finding Methods ---
def bisection(f, a, b, tol=1e-5, max_iter=100):
    """Bisection method for root finding."""
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) and f(b) must have opposite signs.")
    
    for i in range(max_iter):
        c = (a + b) / 2.0
        if f(c) == 0 or (b - a) / 2.0 < tol:
            return c, i+1
        if np.sign(f(c)) == np.sign(f(a)):
            a = c
        else:
            b = c
    return (a + b) / 2.0, max_iter

def newton_raphson(f, df, x0, tol=1e-5, max_iter=100):
    """Newton-Raphson method for root finding."""
    x = x0
    for i in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x, i+1
        dfx = df(x)
        if dfx == 0:
            raise ZeroDivisionError("Derivative is zero. Newton-Raphson failed.")
        x = x - fx / dfx
    return x, max_iter

def secant(f, x0, x1, tol=1e-5, max_iter=100):
    """Secant method for root finding."""
    for i in range(max_iter):
        fx0, fx1 = f(x0), f(x1)
        if abs(fx1) < tol:
            return x1, i+1
        if fx1 - fx0 == 0:
            raise ZeroDivisionError("Secant line is horizontal.")
        x_next = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        x0, x1 = x1, x_next
    return x1, max_iter

# --- 2. Numerical Differentiation ---
def forward_diff(y, h):
    """Forward finite difference."""
    dydx = np.zeros_like(y)
    dydx[:-1] = (y[1:] - y[:-1]) / h
    dydx[-1] = dydx[-2] # Fallback for last element
    return dydx

def backward_diff(y, h):
    """Backward finite difference."""
    dydx = np.zeros_like(y)
    dydx[1:] = (y[1:] - y[:-1]) / h
    dydx[0] = dydx[1] # Fallback for first element
    return dydx

def central_diff(y, h):
    """Central finite difference."""
    dydx = np.zeros_like(y)
    dydx[1:-1] = (y[2:] - y[:-2]) / (2 * h)
    dydx[0] = (y[1] - y[0]) / h         # Forward diff for first
    dydx[-1] = (y[-1] - y[-2]) / h      # Backward diff for last
    return dydx

# --- 3. Numerical Integration ---
def trapezoidal_rule(y, dx):
    """Trapezoidal integration rule."""
    return dx * (np.sum(y) - 0.5 * (y[0] + y[-1]))

def simpson_rule(y, dx):
    """Simpson's 1/3 integration rule (requires odd number of points)."""
    n = len(y)
    if n % 2 == 0:
        # If even, compute Simpson for n-1 and Trapezoidal for the last segment
        s_integ = (dx / 3) * (y[0] + 4 * np.sum(y[1:-2:2]) + 2 * np.sum(y[2:-2:2]) + y[-2])
        trap_integ = 0.5 * dx * (y[-2] + y[-1])
        return s_integ + trap_integ
    return (dx / 3) * (y[0] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2]) + y[-1])

# --- 4. Linear Systems ---
def gaussian_elimination(A, b):
    """Solves Ax = b using Gaussian elimination with partial pivoting."""
    n = len(b)
    M = A.copy().astype(float)
    v = b.copy().astype(float)
    
    # Forward Elimination
    for i in range(n):
        # Partial pivoting
        max_row = np.argmax(abs(M[i:n, i])) + i
        if M[max_row, i] == 0:
            raise ValueError("Matrix is singular.")
        
        M[[i, max_row]] = M[[max_row, i]]
        v[[i, max_row]] = v[[max_row, i]]
        
        for j in range(i + 1, n):
            factor = M[j, i] / M[i, i]
            M[j, i:] -= factor * M[i, i:]
            v[j] -= factor * v[i]
            
    # Back Substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (v[i] - np.dot(M[i, i+1:], x[i+1:])) / M[i, i]
        
    return x