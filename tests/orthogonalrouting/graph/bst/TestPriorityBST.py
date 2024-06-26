
from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase

from orthogonalrouting.graph.Node import Node
from orthogonalrouting.graph.Nodes import Nodes
from orthogonalrouting.graph.interfaces.INode import INode

from orthogonalrouting.graph.bst.IPriorityBST import IPriorityBST
from orthogonalrouting.graph.bst.PriorityBST import PriorityBST
from orthogonalrouting.graph.bst.PriorityBST import PriorityBSTNode


class TestPriorityBST(UnitTestBase):
    """
    Auto generated by the one and only:
        Gato Malo – Humberto A. Sanchez II
        Generated: 17 March 2024
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        nodes: Nodes = Nodes(
            [
                Node(x=500, y=500), Node(x=400, y=600), Node(x=300, y=700), Node(x=600, y=600), Node(x=700, y=700)
            ]
        )

        self._priorityBST: IPriorityBST = PriorityBST()

        self._priorityBST.buildTree(nodes=nodes)
        self._nodes: Nodes = nodes

    def tearDown(self):
        super().tearDown()

    def testFindByeNode(self):
        foundNode: INode = self._priorityBST.find(node=self._nodes[3])
        self.assertEqual(self._nodes[3], foundNode, 'Incorrect Node')

    def testFindByCoordinates(self):

        foundNode: INode = self._priorityBST.find(x=300, y=700)
        self.assertEqual(self._nodes[2], foundNode, 'Incorrect Node')

    def testFindByKey(self):
        foundNode: INode = self._priorityBST.find(key='[300,700]')
        self.assertEqual(self._nodes[2], foundNode, 'Incorrect Node')

    def testBuildTree(self):

        self._inOrderTraversal(self._priorityBST.rootBSTNode, nodeType='Root')

    def _inOrderTraversal(self, bstNode: PriorityBSTNode, nodeType: str):

        if bstNode is not None:
            self._inOrderTraversal(bstNode=bstNode.left, nodeType='Left')
            self.logger.info(f'{nodeType}: {bstNode.data}')
            self._inOrderTraversal(bstNode.right, nodeType='Right')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestPriorityBST))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
