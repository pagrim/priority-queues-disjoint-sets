import pytest

from table_merge import TableMerge

@pytest.mark.parametrize(("table_rows", "merge_operations", "exp_max_rows"),
[
([1, 1, 1, 1, 1], [(3, 5), (2, 4), (1, 4), (5, 4), (5, 3)], [2, 2, 3, 5, 5])
])
def test_merge_fetch_max(table_rows, merge_operations, exp_max_rows):
    tm = TableMerge(row_counts=table_rows)
    assert tm.merge_fetch_max(merge_operations) == exp_max_rows
