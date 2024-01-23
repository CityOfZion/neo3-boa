__all__ = [
    'Oracle',
]


from typing import Any

from boa3.builtin.type import UInt160


class Oracle:
    """
    Neo Oracle Service is an out-of-chain data access service built into Neo N3. It allows users to request the external
    data sources in smart contracts, and Oracle nodes designated by the committee will access the specified data source
    then pass the result in the callback function to continue executing the smart contract logic.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/Advances/Oracles>`__ to learn more about Oracles.
    """
    hash: UInt160

    @classmethod
    def request(cls, url: str, request_filter: str | None, callback: str, user_data: Any, gas_for_response: int):
        """
        Requests an information from outside the blockchain.

        This method just requests data from the oracle, it won't return the result.

        >>> Oracle.request('https://dora.coz.io/api/v1/neo3/testnet/asset/0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5',
        ...                '', 'callback_name', None, 10 * 10 ** 8)
        None

        :param url: External url to retrieve the data
        :type url: str
        :param request_filter:
            Filter to the request.

            See JSONPath format https://github.com/atifaziz/JSONPath

        :type request_filter: str or None
        :param callback:
            Method name that will be as a callback.

            This method must be public and implement the following interface:

            ``(url: str, user_data: Any, code: int, result: bytes) -> None``

        :type callback: str
        :param user_data: Optional data. It'll be returned as the same when the callback is called
        :type user_data: Any
        :param gas_for_response:
            Amount of GAS needed to run the callback method.

            It MUST NOT be specified as the user representation.

            If it costs 1 gas, this value must be 1_00000000 (with the 8 decimals)
        :type gas_for_response: int
        """
        pass

    @classmethod
    def get_price(cls) -> int:
        """
        Gets the price for an Oracle request.

        >>> Oracle.get_price()
        50000000

        :return: the price for an Oracle request
        """
        pass
