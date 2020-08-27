from datetime import datetime
from typing import List


class NodeWeight:
    SPEED_RECORD_COUNT = 3
    SPEED_INIT_VALUE = 100 * 1024 ^ 2  # Start with a big speed of 100 MB/s

    REQUEST_TIME_RECORD_COUNT = 3

    def __init__(self, node_id: int):
        """
        An internal class for tracking and calculating node weight data.

        Is used by ``NodeManager`` for selecting the next node candidate.

        Args:
            node_id: the :attr:`~neo3.network.node.NeoNode.id` of the node this weight belongs to.
        """

        #: The :attr:`~neo3.network.node.NeoNode.id` of the node this weight belongs to.
        self.id: int = node_id

        #: in number of bytes per second
        self.speed: List[float] = [self.SPEED_INIT_VALUE] * self.SPEED_RECORD_COUNT
        self.timeout_count = 0
        self.error_response_count = 0
        now = datetime.utcnow().timestamp() * 1000  # milliseconds
        self.request_time: List[float] = [now] * self.REQUEST_TIME_RECORD_COUNT

    def append_new_speed(self, speed: float) -> None:
        """
        Add a speed value to the collection from which the average speed is calculated.

        The average is calculated based on 3 values. The last value is popped from the collection.

        Args:
            speed: in number of bytes per second
        """
        # remove oldest
        self.speed.pop(-1)
        # add new
        self.speed.insert(0, speed)

    def append_new_request_time(self) -> None:
        """
        Add a request time value to the collection from which the average request time is calculated

        The average is calculated based on 3 values. The last value is popped from the collection.
        """

        self.request_time.pop(-1)

        now = datetime.utcnow().timestamp() * 1000  # milliseconds
        self.request_time.insert(0, now)

    def _avg_speed(self) -> float:
        return sum(self.speed) / self.SPEED_RECORD_COUNT

    def _avg_request_time(self) -> float:
        avg_request_time: float = 0
        now = datetime.utcnow().timestamp() * 1000  # milliseconds

        for t in self.request_time:
            avg_request_time += now - t

        avg_request_time = avg_request_time / self.REQUEST_TIME_RECORD_COUNT
        return avg_request_time

    def weight(self) -> float:
        """
        A score indicating the quality of the node. Higher is better.

        Nodes with the highest speed and the longest time between querying for data have the highest weight
        and will be accessed first by the syncmanager unless their error/timeout count is higher. This distributes the
        load across nodes.
        """
        weight = self._avg_speed() + self._avg_request_time()

        # punish errors and timeouts harder than slower speeds and more recent access
        if self.error_response_count:
            weight /= self.error_response_count + 1  # make sure we at least always divide by 2

        if self.timeout_count:
            weight /= self.timeout_count + 1
        return weight

    def __lt__(self, other):
        return self.weight() < other.weight()

    def __repr__(self):
        return f"<{self.__class__.__name__} at {hex(id(self))}> weight:{self.weight():.2f}"
