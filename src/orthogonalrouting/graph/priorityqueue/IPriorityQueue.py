
from typing import TypeVar


from abc import ABC
from abc import abstractmethod


D = TypeVar('D')


class IPriorityQueue(ABC):

    @property
    @abstractmethod
    def isEmpty(self) -> bool:
        pass

    @property
    @abstractmethod
    def count(self) -> int:
        pass

    @abstractmethod
    def enqueue(self, data: D, priority: int):
        pass

    @abstractmethod
    def dequeue(self) -> D:     # type: ignore
        pass

    @abstractmethod
    def updatePriority(self, node: D, newPriority: int):
        pass

    @abstractmethod
    def contains(self, data: D) -> bool:
        pass

    @abstractmethod
    def peek(self) -> D:    # type: ignore
        pass

    @abstractmethod
    def clear(self):
        pass
