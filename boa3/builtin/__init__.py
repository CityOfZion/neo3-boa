import boa3.builtin.compile_time
import boa3.builtin.contract
import boa3.builtin.interop
import boa3.builtin.math
import boa3.builtin.nativecontract
import boa3.builtin.vm


env: str
"""
Gets the compiled environment. This allows specific environment validations to be easily included in the smart contract 
logic without the need to rewrite anything before compiling (i.e. changes in smart contracts hashes between testnet and 
mainnet). 

>>> # compiling with 'neo3-boa compile -e test_net ./path/to/contract.py'
... from boa3.builtin.interop.contract import call_contract
... from boa3.builtin.type import UInt160
... call_contract(UInt160(b'12345678901234567890') if env == 'test_net' else b'abcdeabcdeabcdeabcde',
...               'balanceOf',
...               UInt160(b'zyxwvzyxwvzyxwvzyxwv'))
110000

>>> # compiling with 'neo3-boa compile -e main_net ./path/to/contract.py'
... from boa3.builtin.interop.contract import call_contract
... from boa3.builtin.type import UInt160
... call_contract(UInt160(b'12345678901234567890') if env == 'test_net' else b'abcdeabcdeabcdeabcde',
...               'balanceOf',
...               UInt160(b'zyxwvzyxwvzyxwvzyxwv'))
250

:meta hide-value:
"""
