from heap import MinHeap
import pytest

@pytest.mark.parametrize(("heap_data", "exp_result"),
[
([1, 2, 3], True),
([3, 2, 1], False),
([2, 3, 5, 1, 4], False),
([2, 3, 5, 4, 6, 8], True)
])
def test_is_heap(heap_data, exp_result):
    mh = MinHeap(data=heap_data)
    assert mh.is_heap() == exp_result

@pytest.mark.parametrize(("heap_data", "exp_swaps"),
[
([5, 4, 3, 2, 1], [(1, 4), (1, 5), (2, 5)]),
([8, 4, 5, 7, 6, 3, 2], [(2, 5), (2, 8), (3, 8)]),
])
def test_build_heap(heap_data, exp_swaps):
    mh = MinHeap(data=heap_data)
    mh.build_heap()
    assert mh.swaps == exp_swaps

@pytest.mark.parametrize(("heap_data"),
[
([3, 4, 5])
])
def test_insert(heap_data):
    mh = MinHeap(data=heap_data)
    assert mh.is_heap()
    mh.insert(2)
    mh.insert(1)
    assert mh.is_heap()
