from typing import Any, Union


class Oracle:

    @classmethod
    def request(cls, url: str, request_filter: Union[str, None], callback: str, user_data: Any, gas_for_response: int):
        """
        Requests an information from outside the blockchain.
        This method just requests data from the oracle, it won't return the result.

        :param url: external url to retrieve the data
        :type url: str
        :param request_filter: filter to the request.
                               See JSONPath format https://github.com/atifaziz/JSONPath
        :type request_filter: str or None
        :param callback: Method name that will be as a callback.
                         This method must be public and implement the following interface:

                         (url: str, user_data: Any, code: int, result: bytes) -> None
        :type callback: str
        :param user_data: optional data. It'll be returned as the same when the callback is called
        :type user_data: Any
        :param gas_for_response: Amount of GAS needed to run the callback method.
                                 It MUST NOT be specified as the user representation.
                                 If it costs 1 gas, this value must be 1_00000000 (with the 8 decimals)
        :type gas_for_response: int
        """
        pass
