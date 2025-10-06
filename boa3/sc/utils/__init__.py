__all__ = [
    "Iterator",
    "env",
    "CreateNewEvent",
    "Nep11TransferEvent",
    "Nep17TransferEvent",
    "to_hex_str",
    "to_script_hash",
    "call_contract",
    "get_call_flags",
    "abort",
    "check_sig",
    "check_multisig",
    "create_standard_account",
    "create_multisig_account",
    "to_bool",
    "to_int",
    "to_bytes",
    "to_str",
    "hash160",
    "hash256",
]

from typing import Any, Sequence

from boa3.sc.types import Event, ECPoint, UInt160, CallFlags
from boa3.sc.utils.iterator import Iterator

env: str = 'compiler'
"""
Gets the compiled environment. This allows specific environment validations to be easily included in the smart contract 
logic without the need to rewrite anything before compiling (i.e. changes in smart contracts hashes between testnet and 
mainnet). 

>>> # compiling with 'neo3-boa compile -e test_net ./path/to/contract.py'
... from boa3.sc.utils import call_contract
... from boa3.sc.types import UInt160
... call_contract(UInt160(b'12345678901234567890') if env == 'test_net' else b'abcdeabcdeabcdeabcde',
...               'balanceOf',
...               UInt160(b'zyxwvzyxwvzyxwvzyxwv'))
110000

>>> # compiling with 'neo3-boa compile -e main_net ./path/to/contract.py'
... from boa3.sc.utils import call_contract
... from boa3.sc.types import UInt160
... call_contract(UInt160(b'12345678901234567890') if env == 'test_net' else b'abcdeabcdeabcdeabcde',
...               'balanceOf',
...               UInt160(b'zyxwvzyxwvzyxwvzyxwv'))
250

:meta hide-value:
"""


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
    :rtype: Event
    """
    pass


Nep11TransferEvent: Event = CreateNewEvent(
    [
        ('from', UInt160 | None),
        ('to', UInt160 | None),
        ('amount', int),
        ('tokenId', str | bytes)
    ],
    'Transfer'
)
"""
The NEP-11 Transfer event that should be triggered whenever a non-fungible token is transferred, minted or burned. It 
needs the addresses of the sender, receiver, amount transferred and the id of the token.

Check out the `proposal <https://github.com/neo-project/proposals/blob/master/nep-11.mediawiki>`__ or 
`Neo's Documentation <https://developers.neo.org/docs/n3/develop/write/nep11>`__ about this NEP.

>>> Nep11TransferEvent(b'\\xd1\\x17\\x92\\x82\\x12\\xc6\\xbe\\xfa\\x05\\xa0\\x23\\x07\\xa1\\x12\\x55\\x41\\x06\\x55\\x10\\xe6',  # when calling, it will return None, but the event will be triggered
...                    b'\\x18\\xb7\\x30\\x14\\xdf\\xcb\\xee\\x01\\x30\\x00\\x13\\x9b\\x8d\\xa0\\x13\\xfb\\x96\\xac\\xd1\\xc0', 1, '01')
{
    'name': 'Transfer',
    'script hash': b'\\x13\\xb4\\x51\\xa2\\x1c\\x10\\x12\\xd6\\x13\\x12\\x19\\x0c\\x15\\x61\\x9b\\x1b\\xd1\\xa2\\xf4\\xb2',
    'state': {
        'from': b'\\xd1\\x17\\x92\\x82\\x12\\xc6\\xbe\\xfa\\x05\\xa0\\x23\\x07\\xa1\\x12\\x55\\x41\\x06\\x55\\x10\\xe6',
        'to': b'\\x18\\xb7\\x30\\x14\\xdf\\xcb\\xee\\x01\\x30\\x00\\x13\\x9b\\x8d\\xa0\\x13\\xfb\\x96\\xac\\xd1\\xc0',
        'amount': 1,
        'tokenId': '01'
    }
}

:meta hide-value:
"""


Nep17TransferEvent: Event = CreateNewEvent(
    [
        ('from', UInt160 | None),
        ('to', UInt160 | None),
        ('amount', int)
    ],
    'Transfer'
)
"""
The NEP-17 Transfer event that should be triggered whenever a fungible token is transferred, minted or burned. It needs
the addresses of the sender, receiver and the amount transferred.

Check out the `proposal <https://github.com/neo-project/proposals/blob/master/nep-17.mediawiki>`__ or 
`Neo's Documentation <https://developers.neo.org/docs/n3/develop/write/nep17>`__ about this NEP.

>>> Nep17TransferEvent(b'\\xd1\\x17\\x92\\x82\\x12\\xc6\\xbe\\xfa\\x05\\xa0\\x23\\x07\\xa1\\x12\\x55\\x41\\x06\\x55\\x10\\xe6',  # when calling, it will return None, but the event will be triggered
...                    b'\\x18\\xb7\\x30\\x14\\xdf\\xcb\\xee\\x01\\x30\\x00\\x13\\x9b\\x8d\\xa0\\x13\\xfb\\x96\\xac\\xd1\\xc0', 100)
{
    'name': 'Transfer',
    'script hash': b'\\x17\\xe3\\xca\\x91\\xca\\xb7\\xaf\\xdd\\xe6\\xba\\x07\\xaa\\xba\\xa1\\x66\\xab\\xcf\\x00\\x04\\x50',
    'state': {
        'from': b'\\xd1\\x17\\x92\\x82\\x12\\xc6\\xbe\\xfa\\x05\\xa0\\x23\\x07\\xa1\\x12\\x55\\x41\\x06\\x55\\x10\\xe6',
        'to': b'\\x18\\xb7\\x30\\x14\\xdf\\xcb\\xee\\x01\\x30\\x00\\x13\\x9b\\x8d\\xa0\\x13\\xfb\\x96\\xac\\xd1\\xc0',
        'amount': 100
    }
}

:meta hide-value:
"""


def to_hex_str(data: bytes) -> str:
    """
    Converts bytes into its string hex representation.

    >>> to_hex_str(ECPoint(bytes(range(33))))
    '201f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100'

    >>> to_hex_str(b'1234567891')
    '31393837363534333231'

    :param data: data to represent as hex.
    :type data: bytearray or bytes

    :return: the hex representation of the data
    :rtype: str
    """
    pass


def to_script_hash(data_bytes: Any) -> bytes:
    """
    Converts a data to a script hash.

    >>> to_script_hash(ECPoint(bytes(range(33))))
    b'\\x12\\xc8z\\xfb3k\\x1e4>\\xb3\\x83\\tK\\xc7\\xdch\\xe5\\xee\\xc7\\x98'

    >>> to_script_hash(b'1234567891')
    b'\\x4b\\x56\\x34\\x17\\xed\\x99\\x7f\\x13\\x22\\x67\\x40\\x79\\x36\\x8b\\xa2\\xcd\\x72\\x41\\x25\\x6d'

    :param data_bytes: data to hash
    :type data_bytes: Any
    :return: the script hash of the data
    :rtype: bytes
    """
    pass


def call_contract(script_hash: UInt160, method: str, args: Sequence = (), call_flags: CallFlags = CallFlags.ALL) -> Any:
    """
    Calls a smart contract given the method and the arguments. Since the return is type Any, you'll probably need to
    type cast the return.

    >>> from boa3.sc.contracts import NeoToken
    ... call_contract(NeoToken.hash, 'balanceOf', [UInt160(b'\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2')])
    100

    :param script_hash: the target smart contract's script hash
    :type script_hash: boa3.sc.types.UInt160
    :param method: the name of the method to be executed
    :type method: str
    :param args: the specified method's arguments
    :type args: Sequence[Any]
    :param call_flags: the CallFlags to be used to call the contract
    :type call_flags: boa3.sc.types.CallFlags

    :return: the result of the specified method
    :rtype: Any

    :raise Exception: raised if there isn't a valid CallFlags, the script hash is not a valid smart contract or the
        method was not found or the arguments aren't valid to the specified method.
    """
    pass


def get_call_flags() -> CallFlags:
    """
    Gets the CallFlags in the current context.

    >>> get_call_flags()
    CallFlags.READ_ONLY
    """
    pass


def abort(msg: str | None = None):
    """
    Aborts the execution of a smart contract. Using this will cancel the changes made on the blockchain by the
    transaction.

    >>> abort()     # abort doesn't return anything by itself, but the execution will stop and the VMState will be FAULT
    VMState.FAULT

    >>> abort('abort message')
    VMState.FAULT

    """
    pass


def check_sig(pub_key: ECPoint, signature: bytes) -> bool:
    """
    Checks the signature for the current script container.

    >>> check_sig(ECPoint(b'\\x03\\x5a\\x92\\x8f\\x20\\x16\\x39\\x20\\x4e\\x06\\xb4\\x36\\x8b\\x1a\\x93\\x36\\x54\\x62\\xa8\\xeb\\xbf\\xf0\\xb8\\x81\\x81\\x51\\xb7\\x4f\\xaa\\xb3\\xa2\\xb6\\x1a'),
    ...           b'wrongsignature')
    False

    :param pub_key: the public key of the account
    :type pub_key: boa3.sc.types.ECPoint
    :param signature: the signature of the current script container
    :type signature: bytes
    :return: whether the signature is valid or not
    :rtype: bool
    """
    pass


def check_multisig(pubkeys: list[ECPoint], signatures: list[bytes]) -> bool:
    """
    Checks the signatures for the current script container.

    >>> check_multisig([ECPoint(b"\\x03\\xcd\\xb0\\x67\\xd9\\x30\\xfd\\x5a\\xda\\xa6\\xc6\\x85\\x45\\x01\\x60\\x44\\xaa\\xdd\\xec\\x64\\xba\\x39\\xe5\\x48\\x25\\x0e\\xae\\xa5\\x51\\x17\\x2e\\x53\\x5c"),
    ...                 ECPoint(b"\\x03l\\x841\\xccx\\xb31w\\xa6\\x0bK\\xcc\\x02\\xba\\xf6\\r\\x05\\xfe\\xe5\\x03\\x8es9\\xd3\\xa6\\x88\\xe3\\x94\\xc2\\xcb\\xd8C")],
    ...                [b'wrongsignature1', b'wrongsignature2'])
    False

    :param pubkeys: a list of public keys
    :type pubkeys: list[boa3.sc.types.ECPoint]
    :param signatures: a list of signatures
    :type signatures: list[bytes]
    :return: a boolean value that represents whether the signatures were validated
    :rtype: bool
    """
    pass


def create_standard_account(pub_key: ECPoint) -> UInt160:
    """
    Calculates the script hash from a public key.

    >>> create_standard_account(ECPoint(b'\\x03\\x5a\\x92\\x8f\\x20\\x16\\x39\\x20\\x4e\\x06\\xb4\\x36\\x8b\\x1a\\x93\\x36\\x54\\x62\\xa8\\xeb\\xbf\\xf0\\xb8\\x81\\x81\\x51\\xb7\\x4f\\xaa\\xb3\\xa2\\xb6\\x1a'))
    b'\\r\\xa9g\\xa4\\x00C+\\xf2\\x7f\\x8e\\x8e\\xb4o\\xe8\\xace\\x9e\\xcc\\xde\\x04'

    :param pub_key: the given public key
    :type pub_key: boa3.sc.types.ECPoint

    :return: the corresponding script hash of the public key
    :rtype: boa3.sc.types.UInt160
    """
    pass


def create_multisig_account(m: int, pub_keys: list[ECPoint]) -> UInt160:
    """
    Calculates corresponding multisig account script hash for the given public keys.

    >>> create_multisig_account(1, [ECPoint(b'\\x03\\x5a\\x92\\x8f\\x20\\x16\\x39\\x20\\x4e\\x06\\xb4\\x36\\x8b\\x1a\\x93\\x36\\x54\\x62\\xa8\\xeb\\xbf\\xf0\\xb8\\x81\\x81\\x51\\xb7\\x4f\\xaa\\xb3\\xa2\\xb6\\x1a')])
    b'"5,\\xd2\\x9e\\xe7\\xb4\\x02\\x08b\\xdbd\\x1e\\xedx\\x82\\x8fU(m'

    :param m: the minimum number of correct signatures need to be provided in order for the verification to pass.
    :type m: int
    :param pub_keys: the public keys of the account
    :type pub_keys: list[boa3.sc.types.ECPoint]

    :return: the hash of the corresponding account
    :rtype: boa3.sc.types.UInt160
    """
    pass


def to_bool(value: bytes) -> bool:
    """
    Return a bytes value to the boolean it represents.

    >>> to_bool(b'\\x00')
    False

    >>> to_bool(b'\\x01')
    True

    >>> to_bool(b'\\x02')
    True
    """
    pass


def to_bytes(value: str | int, length: int = 1, big_endian: bool = True, signed: bool = False) -> bytes:
    """
    Converts a str or integer value to an array of bytes.
    If the value is a string, the other parameters are not valid.
    If the value is an integer, the length of the bytes and whether it's expecting big or little endian representation
    can be specified.
    Throws an exception if the int value is negative or if the length is less than the length of the value in bytes.

    >>> to_bytes(65)
    b'A'

    >>> to_bytes(1234, 3)
    b'\x00\x04\xd2'
    >>> to_bytes(1234, 3, True)
    b'\x00\x04\xd2'
    >>> to_bytes(1234, 3, False)
    b'\xd2\x04\x00'
    >>> to_bytes(-120, 1, False, True)
    b'\x88'

    >>> to_bytes('A')
    b'A'

    :param value: value to be converted to bytes
    :type value: str | int
    :param length: available only to integer values, it represents the length of the resulting bytes
    :type length: int
    :param big_endian: available only to integer values, whether to represent the integer in big-endian (True) or
    little-endian (False) byte order
    :type big_endian: bool
    :param signed: available only to integer values, whether to represent the integer as signed (True) or
    unsigned (False) in bytes return
    :type signed: bool
    :return: a byte value that represents the given value
    :rtype: bytes

    :raise Exception: raised if int value is negative or length is less than the length that the integer value can be represented
    """
    pass


def to_int(value: bytes, big_endian: bool = True, signed: bool = False) -> int:
    """
    Converts a bytes value to the integer it represents.

    >>> to_int(b'A')
    65

    >>> to_int(b'\xfa\x15')
    64021

    >>> to_int(b'\xfa\x15', False)
    5626

    >>> to_int(b'\xfa\x15', True, True)
    -1515

    :param value: value to be converted to int
    :type value: bytes
    :param big_endian: whether to interpret the bytes in big-endian (True) or little-endian (False) byte order
    :type big_endian: bool
    :param signed: whether to interpret the bytes as a signed (True) or unsigned (False) integer
    :type signed: bool
    :return:
    :rtype: int
    """
    pass


def to_str(value: bytes) -> str:
    """
    Converts a bytes value to a string.

    >>> to_str(b'A')
    'A'
    """
    pass


def hash160(key: Any) -> bytes:
    """
    Encrypts a key using HASH160.

    >>> hash160('unit test')
    b'#Q\\xc9\\xaf+c\\x12\\xb1\\xb9\\x9e\\xa1\\x89t\\xa228g\\xec\\x0eF'

    >>> hash160(10)
    b'\\x89\\x86D\\x19\\xa8\\xc3v%\\x00\\xfe\\x9a\\x98\\xaf\\x8f\\xbbO3u\\x08\\xf0'

    :param key: the key to be encrypted
    :type key: Any
    :return: a byte value that represents the encrypted key
    :rtype: bytes
    """
    pass


def hash256(key: Any) -> bytes:
    """
    Encrypts a key using HASH256.

    >>> hash256('unit test')
    b'\\xdau1>J\\xc2W\\xf8LN\\xfb2\\x0f\\xbd\\x01\\x1cr@<\\xf5\\x93<\\x90\\xd2\\xe3\\xb8$\\xd6H\\x96\\xf8\\x9a'

    >>> hash256(10)
    b'\\x9c\\x82r\\x01\\xb9@\\x19\\xb4/\\x85pk\\xc4\\x9cY\\xff\\x84\\xb5`M\\x11\\xca\\xaf\\xb9\\n\\xb9HV\\xc4\\xe1\\xddz'

    :param key: the key to be encrypted
    :type key: Any
    :return: a byte value that represents the encrypted key
    :rtype: bytes
    """
    pass
