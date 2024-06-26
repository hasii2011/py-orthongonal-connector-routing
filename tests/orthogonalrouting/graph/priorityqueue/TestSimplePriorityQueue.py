
from typing import Tuple
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from random import randint

from orthogonalrouting.graph.priorityqueue.IPriorityQueue import IPriorityQueue

from orthogonalrouting.graph.priorityqueue.SimplePriorityQueue import SimplePriorityQueue

from tests.orthogonalrouting.graph.priorityqueue.BaseTestPriorityQueue import BaseTestPriorityQueue
from tests.orthogonalrouting.graph.priorityqueue.BaseTestPriorityQueue import TestData

LARGE_NUMBER_OF_NODES: int = 500
MAX_PRIORITY:          int = 10000


class TestSimplePriorityQueue(BaseTestPriorityQueue):
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
        self._priorityQueue: SimplePriorityQueue = SimplePriorityQueue()

    def tearDown(self):
        super().tearDown()

    def testContains(self):
        ozzeeData: TestData = TestData(name='Ozzee')
        fskData:   TestData = TestData(name='FKS')
        hasiiData: TestData = TestData(name='HASII')

        self._priorityQueue.enqueue(priority=2, data=ozzeeData)
        self._priorityQueue.enqueue(priority=3, data=fskData)
        self._priorityQueue.enqueue(priority=1, data=hasiiData)

        self.assertTrue(self._priorityQueue.contains(ozzeeData))
        self.assertTrue(self._priorityQueue.contains(fskData))
        self.assertTrue(self._priorityQueue.contains(hasiiData))

    def testPeek(self):

        priorityQueue: IPriorityQueue = self._priorityQueue
        priorityQueue = self._enqueueTestData(priorityQueue=priorityQueue)

        testData: TestData = priorityQueue.peek()

        self.assertEqual('Data1', testData.name, 'Incorrect peek')

    def testDequeueEmpty(self):

        noData: TestData = self._priorityQueue.dequeue()

        self.assertEqual(None, noData, 'Should get no data object')

    def testDequeueLast(self):

        ozzeeData: TestData = TestData(name='Ozzee')
        self._priorityQueue.enqueue(data=ozzeeData, priority=22)

        lastData: TestData = self._priorityQueue.dequeue()

        self.assertEqual(ozzeeData, lastData, 'Should get the last one back')

    def testDequeueAll(self):
        priorityQueue: IPriorityQueue = self._priorityQueue
        priorityQueue = self._enqueueTestData(priorityQueue=priorityQueue)

        while priorityQueue.isEmpty is False:
            testData: TestData = priorityQueue.dequeue()
            self.logger.info(f'{testData}')

    def testDoesNotContain(self):

        ozzeeData: TestData = TestData(name='Ozzee')
        fskData:   TestData = TestData(name='FKS')
        hasiiData: TestData = TestData(name='HASII')

        self._priorityQueue.enqueue(priority=200, data=ozzeeData)
        self._priorityQueue.enqueue(priority=300, data=fskData)
        self._priorityQueue.enqueue(priority=100, data=hasiiData)

        removedItem: TestData = self._priorityQueue.dequeue()
        self.assertIsNotNone(removedItem, 'We must have removed something')

        ans: bool = self._priorityQueue.contains(hasiiData)

        self.assertEqual(False, ans, 'Incoherent state')

    def testSimpleUpdatePriority(self):
        ozzeeData: TestData = TestData(name='Ozzee')
        fskData: TestData = TestData(name='FKS')
        hasiiData: TestData = TestData(name='HASII')

        self._priorityQueue.enqueue(priority=2, data=ozzeeData)
        self._priorityQueue.enqueue(priority=3, data=fskData)
        self._priorityQueue.enqueue(priority=1, data=hasiiData)

        self._priorityQueue.updatePriority(node=hasiiData, newPriority=200)

        newLowest: TestData = self._priorityQueue.peek()

        self.assertEqual(ozzeeData, newLowest, 'Priority update did not work!!!')

    def testUpdatePriorityLargeQueue(self):
        priorityQueue: IPriorityQueue = self._priorityQueue
        priorityQueue, testData = self._buildPotentiallyLargePriorityQueue(priorityQueue=priorityQueue)

        self.logger.info(f'Enqueued: {priorityQueue.count} test objects')

        currentLowest: TestData = self._priorityQueue.peek()

        self.logger.info(f'Current lowest: {currentLowest}')
        self.logger.info(f'Data to update to lowest: {testData}')

        self._priorityQueue.updatePriority(node=testData, newPriority=1)

        newHighest: TestData = self._priorityQueue.peek()

        self.logger.info(f'New lowest: {newHighest}')

        self.assertEqual(testData, newHighest, 'Was not updated')

    def _buildPotentiallyLargePriorityQueue(self, priorityQueue: IPriorityQueue) -> Tuple[IPriorityQueue, TestData]:

        testData: TestData = cast(TestData, None)
        for x in range(LARGE_NUMBER_OF_NODES):

            randomPriority: int = randint(1, MAX_PRIORITY)
            testData = TestData(f'TestData{x}')
            self._priorityQueue.enqueue(priority=randomPriority, data=testData)

        return priorityQueue, testData


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestSimplePriorityQueue))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
