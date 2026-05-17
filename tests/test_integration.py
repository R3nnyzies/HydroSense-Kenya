import pytest
import numpy as np
from src.numerical_methods import trapezoidal_rule, simpson_rule

def test_trapezoidal_rule():
    """
    Test trapezoidal rule integration.
    Integral of f(x) = x from 0 to 10 should be exactly 50.
    """
    x = np.linspace(0, 10, 100)
    y = x
    dx = x[1] - x[0]
    
    integral = trapezoidal_rule(y, dx)
    assert integral == pytest.approx(50.0, rel=1e-3)

def test_simpson_rule_odd_points():
    """
    Test Simpson's rule with an odd number of points (standard rule).
    Integral of f(x) = x^2 from 0 to 2 is exactly 8/3 (approx 2.6667).
    """
    x = np.linspace(0, 2, 11)  # 11 points = odd
    y = x**2
    dx = x[1] - x[0]
    
    integral = simpson_rule(y, dx)
    assert integral == pytest.approx(8/3, rel=1e-4)

def test_simpson_rule_even_points():
    """
    Test Simpson's rule with an even number of points (triggering the fallback logic).
    Integral of f(x) = x^2 from 0 to 2 is exactly 8/3.
    """
    x = np.linspace(0, 2, 10)  # 10 points = even
    y = x**2
    dx = x[1] - x[0]
    
    integral = simpson_rule(y, dx)
    assert integral == pytest.approx(8/3, rel=1e-3)