
from typing import cast
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger
from logging import DEBUG

from dataclasses import dataclass

from orthogonalrouting.Common import NOT_SET_INT
from orthogonalrouting.Common import NOT_SET_SENTINEL

from orthogonalrouting.graph.priorityqueue.IPriorityQueue import D
from orthogonalrouting.graph.priorityqueue.IPriorityQueue import IPriorityQueue
from orthogonalrouting.graph.priorityqueue.InvalidOperationException import InvalidOperationException

DEFAULT_CAPACITY: int = 20


@dataclass(kw_only=True, slots=True)
class HeapNode:
    id:              int
    data:            Any = NOT_SET_SENTINEL
    priority:        int = NOT_SET_INT
    positionInQueue: int = NOT_SET_INT


Heap          = NewType('Heap', List[HeapNode])
HeapNodeCache = NewType('HeapNodeCache', Dict[Any, HeapNode])

CmpMethod     = Callable[[int, int], int]

NO_HEAP_NODE: HeapNode = cast(HeapNode, None)

IDX_MAXIMUM_HEAP_ENTRY: int = 1


class PriorityQueue(IPriorityQueue):

    def __init__(self, cmp: CmpMethod):

        self.logger: Logger = getLogger(__name__)

        self._comparer: CmpMethod = cmp

        self._heap: Heap = Heap([])
        self._initializeHeap()

        self._cache:         HeapNodeCache = HeapNodeCache({})
        self._count:         int           = 0
        self._nodeIdCounter: int           = 0

    @property
    def isEmpty(self) -> bool:
        return self._count == 0

    @property
    def count(self) -> int:
        return self._count

    def enqueue(self, data: Any, priority: int):
        if data is None:
            return

        if data in self._cache.keys():
            raise InvalidOperationException(f'Node is already in queue {data}')

        # self._debugPrintHeap('Before enqueue')
        if self._count >= len(self._heap) - 1:
            self._resizeHeap()

        self._count += 1

        heapNode: HeapNode = HeapNode(id=self._nodeIdCounter, data=data, priority=priority, positionInQueue=self._count)
        self._nodeIdCounter += 1
        # self.logger.info(f'New heap node: {heapNode}')
        self._cache[data]       = heapNode
        self._heap[self._count] = heapNode

        self._heapifyUp(heapNode)

        self._debugPrintHeap('after enqueue')

    def dequeue(self) -> D:

        if self.isEmpty is True:
            return cast(D, None)
        elif self._count == 1:
            tmp: D = self._heap[IDX_MAXIMUM_HEAP_ENTRY].data
            self._heap[IDX_MAXIMUM_HEAP_ENTRY] = NO_HEAP_NODE
            self._count = 0

            return tmp

        # TODO:  Might need this for large data sets
        # if self._count < len(self._heap) // 2:
        #     self._shrinkHeap()

        maxPriorityHeapNode:  HeapNode      = self._heap[IDX_MAXIMUM_HEAP_ENTRY]
        lastHeapNode:         HeapNode = self._heap[self._count]

        self._switch(firstIdx=1, secondIdx=self._count)

        lastHeapNode.positionInQueue = 1

        self._heap[self._count] = NO_HEAP_NODE      # this._heap[this.Count] = null;
        self._count -= 1

        del self._cache[maxPriorityHeapNode.data]   # this._cache.Remove(maxPrio.Data);

        self._heapifyDown(heapNode=lastHeapNode)

        return maxPriorityHeapNode.data

    def updatePriority(self, node: D, newPriority: Any):
        pass

    def contains(self, data: Any) -> bool:
        return data in self._cache.keys()

    def peek(self) -> Any:
        if self.isEmpty is True:
            return None         # TODO should return default data type
        else:
            return self._heap[1].data

    def clear(self):
        self._count = 0
        self._heap  = Heap([])
        self._cache = HeapNodeCache({})
        self._initializeHeap()

    def _heapifyUp(self, heapNode: HeapNode):

        if heapNode.positionInQueue < 1:
            return

        parent: int = heapNode.positionInQueue >> 1
        if heapNode.positionInQueue > 1:
            parent = heapNode.positionInQueue >> 1
            if self._isHigherPriority(self._heap[parent], heapNode) is True:
                return
            self._switch(parent=parent, node=heapNode)

        while parent > 1:
            parent = parent // 2
            if self._isHigherPriority(higher=self._heap[parent], lower=heapNode):
                break
            self.logger.debug(f'Switching {self._heap[parent]} and {heapNode}')
            self._switch(parent=parent, node=heapNode)

        self._heap[heapNode.positionInQueue] = heapNode

    def _heapifyDown(self, heapNode: HeapNode):

        lastIndex:    int = heapNode.positionInQueue
        leftChildIdx: int = 2 * lastIndex

        # If leaf do nada'
        if self._isLeaf(leftChildIdx):
            return

        rightChildIdx: int      = leftChildIdx + 1
        leftChild:     HeapNode = self._heap[leftChildIdx]
        rightChild:    HeapNode = self._heap[rightChildIdx]

        # Check if the left-child has higher priority than the current node
        if self._isHigherPriority(higher=leftChild, lower=heapNode) is True:
            # If the right child is leaf, swap and finish
            if self._isLeaf(index=rightChildIdx) is True:

                heapNode.positionInQueue  = leftChildIdx
                leftChild.positionInQueue = lastIndex

                self._heap[lastIndex] = leftChild
                self._heap[leftChildIdx] = heapNode
                return

            # Check if the left-child has higher priority than the right-child
            if self._isHigherPriority(higher=leftChild, lower=rightChild) is True:
                lastIndex = self._moveNode(node=leftChild, childIndex=leftChildIdx, lastIndex=lastIndex)
            else:
                lastIndex = self._moveNode(node=rightChild, childIndex=rightChildIdx, lastIndex=lastIndex)
        elif self._isLeaf(index=rightChildIdx) is True:
            # Return if right child does not exist or is leaf
            return
        else:
            # The Left child is fine, and the node is not a leaf, swap the right child
            if self._isHigherPriority(higher=rightChild, lower=heapNode) is True:
                lastIndex = self._moveNode(node=rightChild, childIndex=rightChildIdx, lastIndex=lastIndex)
            else:
                # Everything is sorted
                return
        #
        while True:
            leftChildIdx = 2 * lastIndex
            # Finish if node is leaf
            if self._isLeaf(leftChildIdx) is True:
                heapNode.positionInQueue = lastIndex
                self._heap[lastIndex]    = heapNode
                break

            # Check if the left-child is higher-priority than the current node
            rightChildIdx = leftChildIdx + 1
            leftChild     = self._heap[leftChildIdx]
            rightChild    = self._heap[rightChildIdx]

            if self._isHigherPriority(higher=leftChild, lower=heapNode) is True:
                # Check if there is a right child. If not, swap and finish.
                if self._isLeaf(index=rightChildIdx):
                    heapNode.positionInQueue  = leftChildIdx
                    leftChild.positionInQueue = lastIndex

                    self._heap[lastIndex]    = leftChild
                    self._heap[leftChildIdx] = heapNode
                    break
                # Check if the left-child is higher-priority than the right-child
                if self._isHigherPriority(higher=leftChild, lower=rightChild) is True:
                    # left is highest, move it up and continue
                    leftChild.positionInQueue = lastIndex
                    self._heap[lastIndex]     = leftChild
                    lastIndex                 = leftChildIdx
                else:
                    # right is even higher, move it up and continue
                    rightChild.positionInQueue = lastIndex
                    self._heap[lastIndex]      = rightChild
                    lastIndex                  = rightChildIdx
            # Not swapping left`-child, does right-child exist?
            elif self._isLeaf(index=rightChildIdx) is True:
                heapNode.positionInQueue = lastIndex
                self._heap[lastIndex]    = rightChild
                lastIndex                = rightChildIdx
            else:
                # Check if right-child is a higher priority than the current node
                if self._isHigherPriority(higher=rightChild, lower=heapNode) is True:
                    rightChild.positionInQueue = lastIndex
                    self._heap[lastIndex]      = rightChild
                    lastIndex                  = rightChildIdx
                else:
                    # Neither child is a higher priority than the current node, so finish and stop
                    heapNode.positionInQueue = lastIndex
                    self._heap[lastIndex]     = heapNode
                    break

    def _isHigherPriority(self, higher: HeapNode, lower: HeapNode) -> bool:

        # Methods a negative number for less-than, zero for equality, or a positive number for greater-than.
        result: int = self._comparer(higher.priority, lower.priority)

        return result < 0 | (result == 0 & higher.id < lower.id)

    def _initializeHeap(self, capacity: int = DEFAULT_CAPACITY):
        self._heap = cast(Heap, [NO_HEAP_NODE] * capacity)

    def _resizeHeap(self):

        oldSize: int  = len(self._heap)
        newSize: int  = oldSize * 2

        for idx in range(oldSize, newSize):
            self._heap.append(NO_HEAP_NODE)

    def _shrinkHeap(self):
        assert False, 'You need to implement this'

    def _switch(self, parent: int = NOT_SET_INT, node: HeapNode = NO_HEAP_NODE, firstIdx: int = NOT_SET_INT, secondIdx: int = NOT_SET_INT):
        """
        Poor man's overloaded method

        TODO: Use multiple dispatch  https://pypi.org/project/multipledispatch/
        Args:
            parent:
            node:
            firstIdx:
            secondIdx:
        """

        if firstIdx == NOT_SET_INT:
            self._switchViaNode(parent=parent, node=node)
        else:
            self._switchViaPriority(firstIdx=firstIdx, secondIdx=secondIdx)

    def _switchViaNode(self, parent: int, node: HeapNode):

        parentNode = self._heap[parent]
        self._heap[node.positionInQueue] = parentNode

        parentNode.positionInQueue = node.positionInQueue
        node.positionInQueue = parent

    def _switchViaPriority(self, firstIdx: int, secondIdx: int):

        tmp: HeapNode = self._heap[firstIdx]

        self._heap[firstIdx] = self._heap[secondIdx]

        self._heap[secondIdx] = tmp

    def _moveNode(self, node: HeapNode, childIndex: int, lastIndex: int) -> int:
        """
        The C# version assumed it could modify the last index;  I changed the
        return signature to return the equivalent value

        Args:
            node:
            childIndex:
            lastIndex:
        """

        node.positionInQueue = lastIndex

        self._heap[lastIndex] = node

        # lastIndex = childIndex    C# was BAD BAD BAD
        return childIndex

    def _isLeaf(self, index: int) -> bool:
        return index > self._count

    def _debugPrintHeap(self, msg: str):

        if self.logger.getEffectiveLevel() == DEBUG:
            self.logger.debug(f'{self._toPrettyHeap(msg=msg)}')

    def _toPrettyHeap(self, msg: str) -> str:
        from os import linesep as osLineSep

        prettyHeap: str = f'{osLineSep}{msg}{osLineSep}'
        for hp in self._heap:
            heapNode: HeapNode = cast(HeapNode, hp)
            if heapNode != NO_HEAP_NODE:
                prettyHeap = f'{prettyHeap}{osLineSep}\t{heapNode.positionInQueue} - {heapNode}'

        return prettyHeap
