
from typing import Any
from typing import Dict
from typing import NewType

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from queue import PriorityQueue
from typing import cast

from nanoid import generate

from orthogonalrouting.Common import NOT_SET_INT
from orthogonalrouting.Common import NOT_SET_SENTINEL

from orthogonalrouting.graph.priorityqueue.IPriorityQueue import D
from orthogonalrouting.graph.priorityqueue.IPriorityQueue import IPriorityQueue
from orthogonalrouting.graph.priorityqueue.InvalidOperationException import InvalidOperationException


@dataclass(kw_only=True, slots=True, order=True)
class HeapNode:
    id:              int
    data:            Any = NOT_SET_SENTINEL
    priority:        int = NOT_SET_INT


HeapNodeCache = NewType('HeapNodeCache', Dict[Any, HeapNode])

QueueTuple = NewType('QueueTuple', tuple[int, Any])


class SimplePriorityQueue(IPriorityQueue):
    """
    Wrap Python's priority queue;  It is a minheap, so we invert the priorities.
    """

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._priorityQueue: PriorityQueue = cast(PriorityQueue, None)
        self._cache:         HeapNodeCache = cast(HeapNodeCache, None)
        # self._nodeIdCounter: int           = NOT_SET_INT

        self._initialize()

    @property
    def isEmpty(self) -> bool:
        return self._priorityQueue.empty()

    @property
    def count(self) -> int:
        return self._priorityQueue.qsize()

    def enqueue(self, data: D, priority: int):
        if data is None:
            return

        if data in self._cache.keys():
            raise InvalidOperationException(f'Data is already enqueue`d {data}')

        nodeId: int = generate(size=8)
        heapNode: HeapNode = HeapNode(id=nodeId, data=data, priority=priority)
        # self._nodeIdCounter += 1

        # self.logger.info(f'New heap node: {heapNode}')
        self._cache[data]      = heapNode
        # Make it  maxheap !!Note the inverted priority
        queueTuple: QueueTuple = QueueTuple((-priority, heapNode))
        self._priorityQueue.put_nowait(queueTuple)

    def dequeue(self) -> D:     # type: ignore

        if self._priorityQueue.empty() is True:
            return cast(D, None)

        queueTuple: QueueTuple = self._priorityQueue.get_nowait()
        heapNode:   HeapNode   = queueTuple[1]
        data: D = heapNode.data

        del self._cache[data]

        return data

    def updatePriority(self, node: D, newPriority: int):
        """
        Update is essentially a very expensive operation.  Given that I am a facade on top
        of a Python built-in that does not support his operation, I am going to use a
        brute-force mechanism where I rebuild the entire AST.

        Args:
            node:
            newPriority:

        """
        self._priorityQueue = PriorityQueue()
        items = self._cache.keys()
        for data in items:
            heapNode: HeapNode = self._cache[data]

            if data == node:
                # Make it  maxheap !!Note the inverted priority
                heapNode.priority  = -newPriority
                queueTuple: QueueTuple = QueueTuple((-newPriority, heapNode))
            else:
                queueTuple: QueueTuple = QueueTuple((heapNode.priority, heapNode))

            self._priorityQueue.put_nowait(queueTuple)

    def contains(self, data: D) -> bool:
        return data in self._cache.keys()

    def peek(self) -> D:    # type: ignore
        """
        This is only safe in single-threaded programs.  Also, I have only validated this
        on Python 3.11.7

        See: https://stackoverflow.com/questions/9287919/can-i-get-an-item-from-a-priorityqueue-without-removing-it-yet

        Returns:  Highest priority item w/o removing it
        """
        queueTuple: QueueTuple = self._priorityQueue.queue[0]
        heapNode:   HeapNode   = queueTuple[1]
        return heapNode.data

    def clear(self):
        self._initialize()

    def _initialize(self):
        self._priorityQueue = PriorityQueue()
        self._cache         = HeapNodeCache({})
        self._nodeIdCounter = 0
