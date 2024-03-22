
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from orthogonalrouting.graph.priorityqueue.IPriorityQueue import IPriorityQueue

from orthogonalrouting.graph.priorityqueue.PriorityQueue import HeapNode
from orthogonalrouting.graph.priorityqueue.PriorityQueue import PriorityQueue

from tests.orthogonalrouting.graph.priorityqueue.BaseTestPriorityQueue import BaseTestPriorityQueue
from tests.orthogonalrouting.graph.priorityqueue.BaseTestPriorityQueue import TestData
from tests.orthogonalrouting.graph.priorityqueue.BaseTestPriorityQueue import TEST_DATA_SIZE


class TestPriorityQueue(BaseTestPriorityQueue):
    """
    Auto generated by the one and only:
        Gato Malo – Humberto A. Sanchez II
        Generated: 18 March 2024
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self._priorityQueue: IPriorityQueue = PriorityQueue(cmp=self._testCmp)

    def tearDown(self):
        super().tearDown()

    def testDequeueEmpty(self):

        noData: TestData = self._priorityQueue.dequeue()

        self.assertEqual(None, noData, 'Should get no data object')

    def testDequeueLast(self):

        ozzeeData: TestData = TestData(name='Ozzee')
        self._priorityQueue.enqueue(data=ozzeeData, priority=22)

        lastData: TestData = self._priorityQueue.dequeue()

        self.assertEqual(ozzeeData, lastData, 'Should get the last one back')

    def testNormalDequeue(self):
        priorityQueue: IPriorityQueue = self._priorityQueue
        priorityQueue = self._enqueueTestData(priorityQueue=priorityQueue)

        cast(PriorityQueue, self._priorityQueue)._debugPrintHeap('Before dequeue')
        testData: TestData = priorityQueue.dequeue()
        cast(PriorityQueue, self._priorityQueue)._debugPrintHeap('After dequeue')
        self.assertIsNotNone(testData, 'Should have been there for me to take out')

    # def testDequeueAll(self):
    #     priorityQueue: IPriorityQueue = self._priorityQueue
    #     priorityQueue = self._enqueueTestData(priorityQueue=priorityQueue)
    #
    #     while priorityQueue.isEmpty is False:
    #         testData: TestData = priorityQueue.dequeue()
    #         self.logger.info(f'{testData}')

    def testPeek(self):

        priorityQueue: IPriorityQueue = self._priorityQueue
        priorityQueue = self._enqueueTestData(priorityQueue=priorityQueue)

        testData: TestData = priorityQueue.peek()

        self.assertEqual('Data10', testData.name, 'Incorrect peek')

    def testEnqueue(self):

        priorityQueue: IPriorityQueue = self._priorityQueue
        priorityQueue = self._enqueueTestData(priorityQueue=priorityQueue)

        self.assertEqual(TEST_DATA_SIZE, priorityQueue.count)

    def testContains(self):
        self._priorityQueue.enqueue(3, 3)
        self._priorityQueue.enqueue(2, 2)
        self._priorityQueue.enqueue(1, 1)

        self.assertTrue(self._priorityQueue.contains(1))
        self.assertTrue(self._priorityQueue.contains(2))
        self.assertTrue(self._priorityQueue.contains(3))

    def testIsHigherPriority(self):

        priorityQueue: PriorityQueue = cast(PriorityQueue, self._priorityQueue)
        higherNode: HeapNode = HeapNode(id=23, data='higherNode', priority=10)
        lowerNode:  HeapNode = HeapNode(id=42, data='lowerNode',  priority=5)

        ans: bool = priorityQueue._isHigherPriority(higher=higherNode, lower=lowerNode)
        self.assertEqual(False, ans, 'Did not calculate correctly')

    def testCmp(self):

        self.assertEqual(-1, self._testCmp(value1=1, value2=3))
        self.assertEqual(0,  self._testCmp(value1=10, value2=10))
        self.assertEqual(1,  self._testCmp(value1=100, value2=10))


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestPriorityQueue))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
