import pytest
import numpy as np
from src.numerical_methods import gaussian_elimination

def test_gaussian_elimination_success():
    """
    Test solving a 3x3 system of linear equations.
    2x + y - z = 8
    -3x - y + 2z = -11
    -2x + y + 2z = -3
    Solution should be x = 2, y = 3, z = -1
    """
    A = np.array([[2, 1, -1], 
                  [-3, -1, 2], 
                  [-2, 1, 2]])
    b = np.array([8, -11, -3])
    
    x = gaussian_elimination(A, b)
    
    assert x[0] == pytest.approx(2.0)
    assert x[1] == pytest.approx(3.0)
    assert x[2] == pytest.approx(-1.0)

def test_gaussian_elimination_singular():
    """Test that a singular matrix raises an appropriate error."""
    # Rows 1 and 2 are identical, causing linear dependence (singular matrix)
    A = np.array([[1, 2, 3], 
                  [1, 2, 3], 
                  [0, 1, 4]])
    b = np.array([1, 1, 1])
    
    with pytest.raises(ValueError, match="Matrix is singular"):
        gaussian_elimination(A, b)