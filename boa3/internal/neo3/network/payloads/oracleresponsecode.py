from enum import IntFlag


class OracleResponseCode(IntFlag):
    """
    Represents the response code for the oracle request.
    """

    SUCCESS = 0x00
    """
    Indicates that the request has been successfully completed.

    :meta hide-value:
    """

    PROTOCOL_NOT_SUPPORTED = 0x10
    """
    Indicates that the protocol of the request is not supported.

    :meta hide-value:
    """

    CONSENSUS_UNREACHABLE = 0x12
    """
    Indicates that the oracle nodes cannot reach a consensus on the result of the request.

    :meta hide-value:
    """

    NOT_FOUND = 0x14
    """
    Indicates that the requested Uri does not exist.

    :meta hide-value:
    """

    TIME_OUT = 0x16
    """
    Indicates that the request was not completed within the specified time.

    :meta hide-value:
    """

    FORBIDDEN = 0x18
    """
    Indicates that there is no permission to request the resource.

    :meta hide-value:
    """

    RESPONSE_TOO_LARGE = 0x1A
    """
    Indicates that the data for the response is too large.

    :meta hide-value:
    """

    INSUFFICIENT_FUNDS = 0x1C
    """
    Indicates that the request failed due to insufficient balance.

    :meta hide-value:
    """

    CONTENT_TYPE_NOT_SUPPORTED = 0x1F
    """
    Indicates that the content-type of the request is not supported.

    :meta hide-value:
    """

    ERROR = 0xFF
    """
    Indicates that the request failed due to other errors.

    :meta hide-value:
    """
