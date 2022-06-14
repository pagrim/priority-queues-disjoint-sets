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

    def union(self, index_i, index_j):
        if index_i == index_j:
            return
        if self.rank[index_i] > self.rank[index_j]:
            self.parent[index_j] = index_i
        else:
            self.parent[index_i] = index_j
            if self.rank[index_i] == self.rank[index_j]:
                self.rank[index_j] += 1


class TableMerge:

    def __init__(self, row_counts):
        self.row_counts = row_counts
        self.set_tree = DisjointSetTree(len(row_counts))

    def merge(self, destination, source):
        dest_idx, src_idx = destination - 1, source - 1
        logging.debug('Candidate merge; destination table %d source table %d', destination, source)
        dest_rows_idx = self.set_tree.find(dest_idx)
        src_rows_idx = self.set_tree.find(src_idx)
        logging.debug('Calculated data rows indices; destination %d source %d', dest_rows_idx, src_rows_idx)
        if dest_rows_idx != src_rows_idx:
            logging.debug('Merging %d with %d', destination, source)
            self.set_tree.union(src_rows_idx, dest_rows_idx)
            logging.debug('Parents %s', self.set_tree.parent)
            logging.debug('Ranks %s', self.set_tree.rank)
            merged_root_idx = self.set_tree.find(src_rows_idx)
            if merged_root_idx == src_rows_idx:
                self.update_row_counts(src_rows_idx, dest_rows_idx)
            else:
                self.update_row_counts(dest_rows_idx, src_rows_idx)

    def update_row_counts(self, root_index, other_index):
        self.row_counts[root_index] += self.row_counts[other_index]
        self.row_counts[other_index] = 0

    def merge_fetch_max(self, merge_ops):
        max_rows = []
        for mo in merge_ops:
            self.merge(*mo)
            logging.debug('Row counts %s', self.row_counts)
            max_rows.append(max(self.row_counts))
        return max_rows


if __name__ == '__main__':
    match_object = re.match(r'(\d+)\s(\d+)', sys.stdin.readline().rstrip())
    num_tables, num_merges = int(match_object.group(1)), int(match_object.group(2))
    row_counts = [int(jb) for jb in sys.stdin.readline().rstrip().split(" ")]

    tm = TableMerge(row_counts=row_counts)
    input_lines = [sys.stdin.readline().rstrip() for _ in range(num_merges)]

    for line in input_lines:
        merge_op = tuple(map(lambda x: int(x), line.split(" ")))
        tm.merge(*merge_op)
        print(max(tm.row_counts))

