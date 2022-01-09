import math
import logging

logging.basicConfig(level=logging.DEBUG)

class MinHeap:

    def __init__(self, data):
        self.heap = data
        self.swaps = []

    def extract_min(self):
        try:
            root = self.heap[0]
        except IndexError:
            root = None
        self.heap[0] = self.heap.pop()
        self.sift_down(0)
        return root

    def is_heap(self):
        for i in range(self.max_comparison_index()):
            logging.debug('Checking node %d', i)
            lc = self.left_child(i)
            rc = self.right_child(i)
            logging.debug('Left child is index is %s', lc)
            logging.debug('Right child is index %s', rc)
            if lc is not None and self.heap[i] >= self.heap[lc]:
                return False
            if rc is not None and self.heap[i] >= self.heap[rc]:
                return False
        return True

    def build_heap(self):
        max_sift_index = self.max_comparison_index()
        for i in range(max_sift_index, -1, -1):
            self.sift_down(i)

    def max_comparison_index(self):
        heap_len = len(self.heap)
        mci = math.floor(heap_len/float(2))
        logging.debug('MCI: %d', mci)
        return mci

    def left_child(self, target_index):
        left_child_pos = (2 * target_index) + 1
        if left_child_pos >= len(self.heap):
            lc = None
        else:
            lc = left_child_pos
        return lc

    def right_child(self, target_index):
        right_child_pos = (2 * target_index) + 2
        if right_child_pos >= len(self.heap):
            rc = None
        else:
            rc = right_child_pos
        return rc


    def sift_down(self, target_index):
        min_index = target_index
        lc = self.left_child(target_index)
        if lc and self.heap[lc] < self.heap[min_index]:
            min_index = lc
        rc = self.right_child(target_index)
        if rc and self.heap[rc] < self.heap[min_index]:
            min_index = rc
        if target_index != min_index:
            logging.info("Swapping position %s with %s; %s -> %s", min_index, target_index, self.heap[min_index], self.heap[target_index])
            self.swaps.append((self.heap[min_index], self.heap[target_index]))
            min_index_val = self.heap[min_index]
            self.heap[min_index] = self.heap[target_index]
            self.heap[target_index] = min_index_val
            self.sift_down(min_index)
