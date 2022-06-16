import pytest

from table_merge import TableMerge, DisjointSetTree


@pytest.mark.parametrize(("table_rows", "merge_operations", "exp_max_rows"),
                         [
                             ([1, 1, 1, 1, 1], [(3, 5), (2, 4), (1, 4), (5, 4), (5, 3)], [2, 2, 3, 5, 5]),
                             ([10, 0, 5, 0, 3, 3], [(6, 6), (6, 5), (5, 4), (4, 3)], [10, 10, 10, 11]),
                             ([1, 1], [(1, 2)], [2])
                         ])
def test_merge_fetch_max(table_rows, merge_operations, exp_max_rows):
    tm = TableMerge(row_counts=table_rows)
    max_rows = tm.merge_fetch_max(merge_operations)
    assert max_rows == exp_max_rows


@pytest.mark.parametrize(('num_objects', 'union_ops', 'find_index', 'exp_res'), [
    (5, [], 2, 2),
    (5, [(4, 2)], 4, 2),
    (5, [(4, 2), (4, 3)], 3, 2),
]
                         )
def test_find(num_objects, union_ops, find_index, exp_res):
    dst = DisjointSetTree(num_objects=num_objects)
    for uo in union_ops:
        dst.union(*uo)
    assert dst.find(find_index) == exp_res



