import pytest
import os
import re

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


@pytest.mark.parametrize('file_name', ["116"])
def test_merge_fetch_max_file(file_name):
    with open(os.path.join('test_data', file_name)) as t:
        match_object = re.match(r'(\d+)\s(\d+)', t.readline().rstrip())
        num_tables, num_merges = int(match_object.group(1)), int(match_object.group(2))
        row_counts = [int(jb) for jb in t.readline().rstrip().split(" ")]

        with open(os.path.join('test_data', f"{file_name}.a")) as a:

            tm = TableMerge(row_counts=row_counts)

            for _ in range(num_merges):
                line = t.readline().rstrip()
                merge_op = tuple(map(lambda x: int(x), line.split(" ")))
                tm.merge_update_max(merge_op)
                exp_max_row_count = int(a.readline().rstrip())

                assert tm.max_row_count == exp_max_row_count


@pytest.mark.parametrize(('num_objects', 'union_ops', 'find_index', 'exp_res'), [
    (5, [], 2, 2),
    (5, [(4, 2)], 4, 2),
    (5, [(4, 2), (4, 3)], 3, 2)
]
                         )
def test_find_set(num_objects, union_ops, find_index, exp_res):
    dst = DisjointSetTree(num_objects=num_objects)
    for uo in union_ops:
        dst.union(*uo)
    assert dst.find_set(find_index) == exp_res


@pytest.mark.parametrize(('num_objects', 'union_ops', 'exp_height'), [
    (8, [(1, 0), (3, 2), (3, 1), (5, 4), (7, 6), (7, 5), (7, 3)], [2, 0, 0, 0, 1, 0, 0, 0])
])
def test_path_compression(num_objects, union_ops, exp_height):
    dst = DisjointSetTree(num_objects=num_objects)
    for uo in union_ops:
        dst.union(*uo)
    comparison = [rnk >= hgt for rnk, hgt in zip(dst.rank, exp_height)]
    assert all(comparison)


