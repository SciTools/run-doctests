"""
Sample module for testing run-doctests.
"""

def function_ok():
    """
    Sample doctest showing correct doctest function.

    Example
    -------
    >>> print(1)
    1
    """
    return 1

def function_bad():
    """
    Sample doctest showing correct doctest function.

    NOTE: 2 fails, as different doctest versions give '1 test' / '1 tests' (!).

    Example
    -------
    >>> print(1)
    0
    >>> 1 == 2
    True
    """
    return 1
