from datetime import datetime


class FlightInfo:
    """
    An internal class for tracking a single outstanding header or block request from a specific node.

    It is used as part of ``SyncManager`` for syncing the chain over the P2P network in combination with the global data
    tracking :class:`RequestInfo <neo3.network.conveniencerequestinfo.RequestInfo>` class.
    """

    def __init__(self, node_id: int, height: int):
        """
        Args:
            node_id: the :attr:`~neo3.network.node.NeoNode.id` of the node the data is requested from
            height: the header or block height being requested
        """

        #: The :attr:`~neo3.network.node.NeoNode.id` of the node the data is requested from.
        #: Defaults to `node_id` parameter.
        self.node_id = node_id

        #: The header or block height being requested.
        #: Defaults to `height` parameter.
        self.height = height

        #: float: UTC timestamp when the instance was created.
        self.start_time: float = datetime.utcnow().timestamp()

    def reset_start_time(self) -> None:
        """ Reset the flight start time."""
        self.start_time = datetime.utcnow().timestamp()
