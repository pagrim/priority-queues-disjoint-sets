class DisjointSetTree:

    def __init__(self, num_objects):
        self.parent = [None for _ in range(num_objects)]
        self.rank = [None for _ in range(num_objects)]
        for index in range(num_objects):
            self.make_set(index)

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
