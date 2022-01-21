from disjoint_set_tree import DisjointSetTree

import logging
logging.basicConfig(level=logging.DEBUG)

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
