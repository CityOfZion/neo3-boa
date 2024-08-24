from boa3.internal.deprecation import deprecated


@deprecated(details='This module is deprecated. Use :mod:`boa3.sc.math` instead')
def ceil(x: int, decimals: int) -> int:
    """
    Return the ceiling of x given the amount of decimals.
    This is the smallest integer >= x.

    >>> ceil(12345, 3)
    13000

    :param x: any integer number
    :type x: int
    :param decimals: number of decimals
    :type decimals: int
    :return: the ceiling of x
    :rtype: int

    :raise Exception: raised when decimals is negative.
    """
    pass


@deprecated(details='This module is deprecated. Use :mod:`boa3.sc.math` instead')
def floor(x: int, decimals: int) -> int:
    """
    Return the floor of x given the amount of decimals.
    This is the largest integer <= x.

    >>> floor(12345, 3)
    12000

    :param x: any integer number
    :type x: int
    :param decimals: number of decimals
    :type decimals: int
    :return: the floor of x
    :rtype: int

    :raise Exception: raised when decimals is negative.
    """
    pass


@deprecated(details='This module is deprecated. Use :mod:`boa3.sc.math` instead')
def sqrt(x: int) -> int:
    """
    Gets the square root of a number.

    >>> sqrt(1)
    1

    >>> sqrt(10)
    3

    >>> sqrt(25)
    5

    :param x: a non-negative number
    :type x: int
    :return: the square root of a number
    :rtype: int

    :raise Exception: raised when number is negative.
    """
    pass
