
from unittest import TestSuite
from unittest import main as unitTestMain

from dataclasses import dataclass
from codeallybasic.UnitTestBase import UnitTestBase

from orthogonalrouting.graph.priorityqueue.IPriorityQueue import IPriorityQueue

TEST_DATA_SIZE: int = 10


@dataclass(eq=False)
class TestData:
    name: str = ''

    def __eq__(self, other) -> bool:

        ans: bool = False
        if isinstance(other, TestData) is True:
            if self.name == other.name:
                ans = True

        return ans

    def __hash__(self):
        return hash(str(self))


class BaseTestPriorityQueue(UnitTestBase):
    """
    Auto generated by the one and only:
        Gato Malo – Humberto A. Sanchez II
        Generated: 21 March 2024
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def _testCmp(self, value1: int, value2) -> int:
        """
        A comparison function is any callable that accept two arguments, compares them
        Args:
            value1:
            value2:

        Returns:  a negative number for less-than, zero for equality, or a positive number for greater-than.

        """
        if value1 < value2:
            return -1

        if value1 == value2:
            return 0

        return 1

    def _enqueueTestData(self, priorityQueue: IPriorityQueue) -> IPriorityQueue:

        for idx in range(TEST_DATA_SIZE):
            priorityQueue.enqueue(data=TestData(name=f'Data{idx+1}'), priority=TEST_DATA_SIZE - idx)

        return priorityQueue


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=BaseTestPriorityQueue))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
