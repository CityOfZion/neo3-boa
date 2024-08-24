__all__ = [
    'CreateNewEvent',
    'public',
    'contract',
    'display_name',
    'NeoMetadata',
]

from boa3.builtin.type import Event
from boa3.internal.deprecation import deprecated
from boa3.sc.compiletime import NeoMetadata


@deprecated(details='This module is deprecated. Use :mod:`boa3.sc.utils` instead')
def CreateNewEvent(arguments: list[tuple[str, type]] = [], event_name: str = '') -> Event:
    """
    Creates a new Event.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/develop/write/basics#events>`__ to learn more
    about Events.

    >>> new_event: Event = CreateNewEvent(
    ...     [
    ...        ('name', str),
    ...        ('amount', int)
    ...     ],
    ...     'New Event'
    ... )

    :param arguments: the list of the events args' names and types
    :type arguments: list[tuple[str, type]]
    :param event_name: custom name of the event. It's filled with the variable name if not specified
    :type event_name: str
    :return: the new event
    :rtype: boa3.builtin.type.Event
    """
    pass


@deprecated(details='This module is deprecated. Use :mod:`boa3.sc.compiletime` instead')
def public(name: str = None, safe: bool = False, *args, **kwargs):
    """
    This decorator identifies which methods should be included in the abi file. Adding this decorator to a function
    means it could be called externally.

    >>> @public     # this method will be added to the abi
    ... def callable_function() -> bool:
    ...     return True
    {
        "name": "callable_function",
        "offset": 0,
        "parameters": [],
        "safe": false,
        "returntype": "Boolean"
    }

    >>> @public(name='callableFunction')     # the method will be added with the different name to the abi
    ... def callable_function() -> bool:
    ...     return True
    {
        "name": "callableFunction",
        "offset": 0,
        "parameters": [],
        "safe": false,
        "returntype": "Boolean"
    }

    >>> @public(safe=True)      # the method will be added with the safe flag to the abi
    ... def callable_function() -> bool:
    ...     return True
    {
        "name": "callable_function",
        "offset": 0,
        "parameters": [],
        "safe": true,
        "returntype": "Boolean"
    }

    :param name: Identifier for this method that'll be used on the abi. If not specified, it'll be the same
     identifier from Python method definition
    :type name: str
    :param safe: Whether this method is an abi safe method. False by default
    :type safe: bool
    """
    def decorator_wrapper(*args, **kwargs):
        pass
    return decorator_wrapper


@deprecated(details='This module is deprecated. Use :mod:`boa3.sc.compiletime` instead')
def contract(script_hash: str | bytes):
    """
    This decorator identifies a class that should be interpreted as an interface to an existing contract.

    If you want to use the script hash in your code, you can use the `hash` class attribute that automatically maps the
    script hash parameter onto it. You don't need to declare it in your class, but your IDE might send a warning about
    the attribute if you don't.

    Check out `Our Documentation <https://dojo.coz.io/neo3/boa/calling-smart-contracts.html#with-interface>`__ to learn
    more about this decorator.

    >>> @contract('0xd2a4cff31913016155e38e474a2c06d08be276cf')
    ... class GASInterface:
    ...     hash: UInt160      # you don't need to declare this class variable, we are only doing it to avoid IDE warnings
    ...                        # but if you do declare, you need to import the type UInt160 from boa3.builtin.type
    ...     @staticmethod
    ...     def symbol() -> str:
    ...         pass
    ... @public
    ... def main() -> str:
    ...     return "Symbol is " + GASInterface.symbol()
    ... @public
    ... def return_hash() -> UInt160:
    ...     return GASInterface.hash    # neo3-boa will understand that this attribute exists even if you don't declare it

    :param script_hash: Script hash of the interfaced contract
    :type script_hash: str or bytes
    """
    def decorator_wrapper(cls, *args, **kwargs):
        if isinstance(script_hash, str):
            from boa3.internal.neo import from_hex_str
            _hash = from_hex_str(script_hash)
        else:
            _hash = script_hash

        cls.hash = _hash
        return cls
    return decorator_wrapper


@deprecated(details='This module is deprecated. Use :mod:`boa3.sc.compiletime` instead')
def display_name(name: str):
    """
    This decorator identifies which methods from a contract interface should have a different identifier from the one
    interfacing it. It only works in contract interface classes.

    >>> @contract('0xd2a4cff31913016155e38e474a2c06d08be276cf')
    ... class GASInterface:
    ...     @staticmethod
    ...     @display_name('totalSupply')
    ...     def total_supply() -> int:      # the smart contract will call "totalSupply", but when writing the script you can call this method whatever you want to
    ...         pass
    ... @public
    ... def main() -> int:
    ...     return GASInterface.total_supply()

    :param name: Method identifier from the contract manifest.
    :type name: str
    """
    def decorator_wrapper(*args, **kwargs):
        pass
    return decorator_wrapper
