import pytest

from disjoint_set_tree import DisjointSetTree

@pytest.fixture
def mock_data():
    return [1,2,3,4,5]

@pytest.fixture
def mock_dst(mock_data):
    return DisjointSetTree(num_objects=len(mock_data))

def test_init(mock_data, mock_dst):
    for i, _ in enumerate(mock_data):
        assert mock_dst.parent[i] == i and mock_dst.rank[i] == 0

def test_union(mock_dst):
    mock_dst.union(0, 1)
    mock_dst.union(1, 2)
    assert mock_dst.parent[0] == 1 and mock_dst.parent[2] == 1
    assert mock_dst.rank[0] == 0 and mock_dst.rank[2] == 0 and mock_dst.rank[1] == 1

def test_union_find(mock_dst):
    mock_dst.union(0, 1)
    mock_dst.union(1, 2)
    assert mock_dst.find(0) == mock_dst.find(1) == mock_dst.find(2) == 1
