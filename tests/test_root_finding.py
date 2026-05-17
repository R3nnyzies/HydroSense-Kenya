import pytest
from src.numerical_methods import bisection, newton_raphson, secant

# Test function: f(x) = x^2 - 4 (Roots at x = 2 and x = -2)
def f(x):
    return x**2 - 4

def df(x):
    return 2*x

def test_bisection_success():
    """Test if bisection method correctly finds the positive root x=2."""
    root, iterations = bisection(f, 0, 5, tol=1e-5)
    assert root == pytest.approx(2.0, abs=1e-4)

def test_bisection_invalid_bounds():
    """Test if bisection method raises an error when bounds do not bracket the root."""
    with pytest.raises(ValueError, match="opposite signs"):
        bisection(f, 3, 5)  # Both f(3) and f(5) are positive

def test_newton_raphson_success():
    """Test if Newton-Raphson method correctly finds the positive root x=2."""
    root, iterations = newton_raphson(f, df, 5, tol=1e-5)
    assert root == pytest.approx(2.0, abs=1e-4)

def test_newton_raphson_zero_derivative():
    """Test if Newton-Raphson handles zero derivative exceptions."""
    with pytest.raises(ZeroDivisionError, match="Derivative is zero"):
        # Derivative of x^2 - 4 at x=0 is 0
        newton_raphson(f, df, 0, tol=1e-5)

def test_secant_success():
    """Test if Secant method correctly finds the positive root x=2."""
    root, iterations = secant(f, 4, 5, tol=1e-5)
    assert root == pytest.approx(2.0, abs=1e-4)