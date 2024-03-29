
from typing import cast
from typing import Any

from logging import Logger
from logging import getLogger

from copy import deepcopy

from dataclasses import dataclass

from orthogonalrouting.graph.Node import NO_NODE
from orthogonalrouting.graph.Node import Node
from orthogonalrouting.graph.interfaces.INode import INode

from orthogonalrouting.graph.Nodes import Nodes

from orthogonalrouting.graph.bst.IPriorityBST import IPriorityBST

NO_PRIORITY_BST_NODE: 'PriorityBSTNode' = cast('PriorityBSTNode', None)


@dataclass
class PriorityBSTNode:

    data:    Any              = None
    border:  int              = 0
    parent: 'PriorityBSTNode' = NO_PRIORITY_BST_NODE
    left:   'PriorityBSTNode' = NO_PRIORITY_BST_NODE
    right:  'PriorityBSTNode' = NO_PRIORITY_BST_NODE


class PriorityBST(IPriorityBST):

    def __init__(self):

        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._root:  PriorityBSTNode = NO_PRIORITY_BST_NODE
        self._count: int             = 0
        self._nodes: Nodes           = Nodes([])

    @property
    def rootBSTNode(self) -> PriorityBSTNode:
        return self._root

    @property
    def root(self) -> INode:
        return self._root.data

    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self, count: int):
        self._count = count

    @property
    def isEmpty(self) -> bool:

        ans: bool = False
        if self._count == 0 and self._root is None:
            ans = True

        return ans

    @property
    def nodes(self) -> Nodes:
        return self._nodes

    @nodes.setter
    def nodes(self, nodes: Nodes):
        self._nodes = nodes

    def buildTree(self, nodes: Nodes):

        if nodes is None or len(nodes) == 0:
            return
        self.clear()
        self.count = len(nodes)
        self.nodes = nodes

        # orderedNodes = nodes.OrderBy(node= > node.Y).ToList();
        orderedNodes: Nodes = deepcopy(nodes)
        orderedNodes.sort(key=self._nodeSortY)
        # var last = orderedNodes.Last();
        last: INode = orderedNodes[-1]
        self._root = PriorityBSTNode(data=last)

        # orderedNodes.Remove(last);
        orderedNodes = cast(Nodes, orderedNodes[:-1])

        if len(orderedNodes) == 0:
            self._root.border = self._root.data.x
        else:
            orderedNodes.sort(key=self._nodeSortX)
            median: int = len(orderedNodes) // 2
            self._root.border = orderedNodes[median].x

            # Where(x => x.X >= 0 && x.X <= _root.Border)
            # noinspection PyChainedComparisons
            subNodes1: Nodes = cast(Nodes, [node for node in orderedNodes if node.x >= 0 and node.x <= self._root.border])
            self._buildSubTree(nodes=subNodes1, parent=self._root, isLeft=True)

            # Where(x => x.X > _root.Border),
            subNodes2: Nodes = cast(Nodes, [node for node in orderedNodes if node.x > self._root.border])
            self._buildSubTree(nodes=subNodes2, parent=self._root, isLeft=False)

    def find(self, x: int = -1, y: int = -1, key: Any = None, node: INode = None) -> Node:
        """
        My version of overloading from the original C# code

        Args:
            x:
            y:
            key:
            node:

        Returns:
        """
        if key is not None:
            return self._findByKey(key=key)
        elif node is not None:
            return self._findByNode(searchNode=node)
        else:
            assert x != -1 and y != -1, 'I do not know which method you want to call'
            return self._findByCoordinates(x=x, y=y)

    def intervalFind(self, x1: int, y1: int, x2: int, y2: int) -> Nodes:
        return self._intervalFind(x1=x1, y1=y1, x2=x2, y2=y2, bstNode=self._root)

    def contains(self, node: INode) -> bool:
        return node in self._nodes

    def insert(self, node: INode):
        if node is None:
            return
        self._nodes.append(node)
        self.buildTree(nodes=self._nodes)

    def remove(self, node: INode):
        if node is None:
            return
        self._nodes.remove(node)
        self.buildTree(nodes=self._nodes)

    def clear(self):
        self._count = 0
        self._root  = NO_PRIORITY_BST_NODE
        self._nodes.clear()

    def toList(self) -> Nodes:
        return self._nodes

    def _buildSubTree(self, nodes: Nodes, parent: PriorityBSTNode, isLeft: bool):
        if len(nodes) == 0:
            return

        nodes.sort(key=self._nodeSortY)
        orderedNodes: Nodes = deepcopy(nodes)
        last:         INode = orderedNodes[-1]
        if isLeft is True:
            parent.left = PriorityBSTNode(data=last, parent=parent)
        else:
            parent.right = PriorityBSTNode(data=last, parent=parent)

        # orderedNodes.Remove(last);
        orderedNodes = cast(Nodes, orderedNodes[:-1])

        if len(orderedNodes) == 0:
            if isLeft is True:
                parent.left.border = parent.left.data.x
            else:
                parent.right.border = parent.right.data.x
        else:
            # orderedNodes = orderedNodes.OrderBy(node => node.X).ToList();
            orderedNodes.sort(key=self._nodeSortX)
            median: int = len(orderedNodes) // 2
            if isLeft is True:
                parent.left.border = orderedNodes[median].x
                # Where(x= > x.X >= 0 & & x.X <= parent.Left.Border),
                # noinspection PyChainedComparisons
                subNodes1: Nodes = cast(Nodes, [node for node in orderedNodes if node.x >= 0 and node.x <= parent.left.border])
                self._buildSubTree(nodes=subNodes1, parent=parent.left, isLeft=True)

                # Where(x= > x.X > parent.Left.Border), parent.Left
                subNodes2: Nodes = cast(Nodes, [node for node in orderedNodes if node.x > parent.left.border])
                self._buildSubTree(nodes=subNodes2, parent=parent.left, isLeft=False)
            else:
                parent.right.border = orderedNodes[median].x
                # Where(x => x.X >= 0 && x.X <= parent.Right.Border)
                # noinspection PyChainedComparisons
                subNodes3: Nodes = cast(Nodes, [node for node in orderedNodes if node.x >= 0 and node.x <= parent.right.border])
                self._buildSubTree(nodes=subNodes3, parent=parent.right, isLeft=True)
                # Where(x => x.X > parent.Right.Border)
                subNodes4: Nodes = cast(Nodes, [node for node in orderedNodes if node.x > parent.right.border])
                self._buildSubTree(nodes=subNodes4, parent=parent.right, isLeft=False)

    def _nodeSortY(self, e: INode):
        return e.y

    def _nodeSortX(self, e: INode):
        return e.x

    def _findByCoordinates(self, x: int, y: int) -> Node:

        current: PriorityBSTNode = self._root
        while True:
            if current is None:
                return NO_NODE
            if current.data.x == x and current.data.y == y:
                return current.data
            if current.data.y < y:
                return NO_NODE
            if current.border >= x:
                current = current.left
            else:
                current = current.right

    def _findByKey(self, key: Any) -> Node:

        findList = [node for node in self._nodes if node.key == key]

        if len(findList) == 1:
            return findList[0]
        else:
            return NO_NODE

    def _findByNode(self, searchNode: INode) -> Node:

        findList = [node for node in self._nodes if node == searchNode]
        if len(findList) == 1:
            return findList[0]
        else:
            return NO_NODE

    # noinspection PyChainedComparisons
    def _intervalFind(self, x1: int, y1: int, x2: int, y2: int, bstNode: PriorityBSTNode) -> Nodes:

        nodes: Nodes = Nodes([])

        if bstNode is None:
            pass
        else:
            if bstNode.data.x >= x1 and bstNode.data.x <= x2 and bstNode.data.y >= y1 and bstNode.data.y <= y2:
                nodes.append(bstNode.data)

            if bstNode.left is not None and y1 <= bstNode.data.y and x1 <= bstNode.border:
                nodes.addRange(self._intervalFind(x1, y1, x2, y2, bstNode.left))

            if bstNode.right is not None and y1 <= bstNode.data.y and x2 > bstNode.border:
                nodes.addRange(self._intervalFind(x1, y1, x2, y2, bstNode.right))

        return nodes
