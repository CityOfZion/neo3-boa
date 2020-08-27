import hashlib
from typing import List, Optional

from boa3.neo3.core import types


class _MerkleTreeNode:
    def __init__(self, hash: types.UInt256 = None):
        self.hash = hash if hash else types.UInt256.zero()  # type: types.UInt256
        self.parent = None  # type: Optional[_MerkleTreeNode]
        self.left_child = None  # type: Optional[_MerkleTreeNode]
        self.right_child = None  # type: Optional[_MerkleTreeNode]

    def is_leaf(self) -> bool:
        """
        Return `True` if the node is a leaf.
        """
        return self.left_child is None and self.right_child is None

    def is_root(self) -> bool:
        """
        Return `True` if the node is the root node.
        """
        return self.parent is None


class MerkleTree:
    def __init__(self, hashes: List[types.UInt256]):
        """

        Args:
            hashes: the list of hashes to build the tree from.

        Raises:
            ValueError: if the `hashes` list is empty.
        """
        if len(hashes) == 0:
            raise ValueError("Hashes list can't empty")

        self.root = self._build(leaves=[_MerkleTreeNode(h) for h in hashes])
        _depth = 1
        i = self.root
        while i.left_child is not None:
            _depth += 1
            i = i.left_child
        self.depth = _depth

    def to_hash_array(self) -> List[types.UInt256]:
        """
        Create a list of hashes the Merkle tree is build up from.

        Note: does not include the Merkle root hash.
        """
        hashes: List[types.UInt256] = []
        MerkleTree._depth_first_search(self.root, hashes)
        return hashes

    @staticmethod
    def _depth_first_search(node: _MerkleTreeNode, hashes: List[types.UInt256]) -> None:
        # if left is None then Right is also always None, but it helps the static type checker understand this
        # otherwise it thinks it might go to the else branch and the second call is then invalid
        if node.left_child is None or node.right_child is None:
            hashes.append(node.hash)
        else:
            MerkleTree._depth_first_search(node.left_child, hashes)
            MerkleTree._depth_first_search(node.right_child, hashes)

    @staticmethod
    def _build(leaves: List[_MerkleTreeNode]) -> _MerkleTreeNode:
        if len(leaves) == 0:
            raise ValueError('Leaves must have length')
        if len(leaves) == 1:
            return leaves[0]

        num_parents = int((len(leaves) + 1) / 2)
        parents = [_MerkleTreeNode() for i in range(0, num_parents)]

        for i in range(0, num_parents):
            node = parents[i]
            node.left_child = leaves[i * 2]
            leaves[i * 2].parent = node
            if (i * 2 + 1 == len(leaves)):
                node.right_child = node.left_child
            else:
                node.right_child = leaves[i * 2 + 1]
                leaves[i * 2 + 1].parent = node

            data = node.left_child.hash.to_array() + node.right_child.hash.to_array()
            hashed_data = hashlib.sha256(hashlib.sha256(data).digest()).digest()
            node.hash = types.UInt256(data=hashed_data)

        return MerkleTree._build(parents)

    @staticmethod
    def compute_root(hashes: List[types.UInt256]) -> types.UInt256:
        """
        Compute the Merkle root hash from a list of hashes.

        Args:
            hashes:

        Raises:
             ValueError: if the `hashes` list is empty.
        """
        if len(hashes) == 1:
            return hashes[0]
        tree = MerkleTree(hashes)
        return tree.root.hash
