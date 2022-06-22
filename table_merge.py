import logging
import re
import sys

logging.basicConfig()


class DisjointSetTree:

    def __init__(self, num_objects):
        self.parent = []
        self.rank = []
        self.make_set_all(num_objects)

    def make_set_all(self, num_objects):
        self.parent = [i for i in range(num_objects)]
        self.rank = [0 for _ in range(num_objects)]

    def make_set(self, index):
        self.parent[index] = index
        self.rank[index] = 0

    def find(self, index):
        while index != self.parent[index]:
            index = self.parent[index]
        return index

    def find_set(self, index):
        root_index = self.find(index)
        self.parent[index] = root_index
        return root_index

    def union(self, index_i, index_j):
        root_i, root_j = self.find_set(index_i), self.find_set(index_j)
        logging.debug('Found root of %d is %d and root of %d is %d', index_i, root_i, index_j, root_j)
        if root_i == root_j:
            return root_i, root_j, None
        if self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
            parent = 0
        else:
            self.parent[root_i] = root_j
            parent = 1
            if self.rank[root_i] == self.rank[root_j]:
                self.rank[root_j] += 1
        logging.debug('Parents after union %s', self.parent)
        logging.debug('Ranks after union %s', self.rank)
        return root_i, root_j, parent


class TableMerge:

    def __init__(self, row_counts):
        self.row_counts = row_counts
        self.set_tree = DisjointSetTree(len(row_counts))
        self.max_row_count = max(self.row_counts)

    def merge(self, destination, source):
        src_idx, dest_idx = source - 1, destination - 1
        logging.debug('Candidate merge; destination table index %d source table index %d', dest_idx, src_idx)
        dest_rows_idx, src_rows_idx, parent_flag = self.set_tree.union(src_idx, dest_idx)
        if parent_flag == 1:
            merged_root_idx = src_rows_idx
            self.update_row_counts(src_rows_idx, dest_rows_idx)
        elif parent_flag == 0:
            merged_root_idx = dest_rows_idx
            self.update_row_counts(dest_rows_idx, src_rows_idx)
        else:
            merged_root_idx = src_rows_idx
        return merged_root_idx

    def update_row_counts(self, root_index, other_index):
        if root_index != other_index:
            self.row_counts[root_index] += self.row_counts[other_index]
            self.row_counts[other_index] = 0

    def merge_update_max(self, merge_op):
        merged_root_idx = self.merge(*merge_op)
        logging.debug('Merged root index %d', merged_root_idx)
        if self.row_counts[merged_root_idx] > self.max_row_count:
            self.max_row_count = self.row_counts[merged_root_idx]


if __name__ == '__main__':
    match_object = re.match(r'(\d+)\s(\d+)', sys.stdin.readline().rstrip())
    num_tables, num_merges = int(match_object.group(1)), int(match_object.group(2))
    row_counts = [int(jb) for jb in sys.stdin.readline().rstrip().split(" ")]

    tm = TableMerge(row_counts=row_counts)

    for _ in range(num_merges):
        line = sys.stdin.readline().rstrip()
        merge_op = tuple(map(lambda x: int(x), line.split(" ")))
        tm.merge_update_max(merge_op)
        print(tm.max_row_count)

