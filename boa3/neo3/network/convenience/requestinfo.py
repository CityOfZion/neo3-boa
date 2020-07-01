from typing import Dict, Optional

from .flightinfo import FlightInfo


class RequestInfo:
    """An internal class for tracking an outstanding header or block request over all connected nodes.

    It is used as part of ``SyncManager`` for syncing the chain over the P2P network.
    For each header or block being requested from the network, 1 RequestInfo object is created. Each RequestInfo stores
    the data to track outstanding flights (=requests from connected nodes).
    """

    def __init__(self, height: int):
        """
        Args:
            height: the header or block height being tracked.
        """
        #: The header or block height being tracked.
        self.height: int = height

        #: A _dictionary holding node :attr:`~neo3.network.node.NeoNode.id` keys, with UTC timestamp values.
        self.failed_nodes: Dict[int, int] = dict()

        #: The total count of flights for this request that failed to meet the time requirements.
        self.failed_total: int = 0

        #: A _dictionary holding node_id keys with :class:`FlightInfo <neo3.network.convenience.flightinfo.FlightInfo>`
        # object values.
        self.flights: Dict[int, FlightInfo] = dict()

        #: The :attr:`~neo3.network.node.NeoNode.id` of the node last used for a flight.
        self.last_used_node: int = -1

    def add_new_flight(self, flight_info: FlightInfo) -> None:
        """
        Store a new flight to the tracking list.

        Args:
            flight_info: the flight to add.
        """
        self.flights[flight_info.node_id] = flight_info
        self.last_used_node = flight_info.node_id

    def most_recent_flight(self) -> Optional[FlightInfo]:
        """
        Get the last :class:`FlightInfo <neo3.network.convenience.flightinfo.FlightInfo>` object created for this
        request.
        """
        try:
            return self.flights[self.last_used_node]
        except KeyError:
            return None

    def mark_failed_node(self, node_id: int) -> None:
        """
        Tag a node for failure.

        SyncManager tags nodes that do not return the requested data before a specified timeout.

        Args:
            node_id: the :attr:`~neo3.network.node.NeoNode.id` of the node the data is requested from.
        """
        self.failed_nodes[node_id] = self.failed_nodes.get(node_id, 0) + 1
        self.failed_total += 1
