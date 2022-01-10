from heap import MinHeap
from dataclasses import dataclass

class ThreadJob:

    def __init__(self, thread_id, start_time, finish_time):
        self.thread_id = thread_id
        self.start_time = start_time
        self.finish_time = finish_time

    def __lt__(self, other):
        if self.finish_time < other.finish_time:
            return True
        elif self.finish_time == other.finish_time:
            return self.thread_id < other.thread_id
        else:
            return False

    def __repr__(self):
        return '({})'.format(', '.join(['{}:{}'.format(k, v) for k, v in self.__dict__.items() if not k.startswith('_')]))

    def __eq__(self, other):
        return self.thread_id == other.thread_id and self.start_time == other.start_time


class ParallelProcessor:

    def __init__(self, jobs, num_threads):
        self.jobs = jobs
        self.thread_heap = MinHeap([ThreadJob(thread_id=i, start_time=None, finish_time=0) for i in range(num_threads)])

    def process(self):
        results = []
        while len(self.jobs) > 0:
            job_processing_time = self.jobs.pop(0)
            next_thread = self.thread_heap.extract_min()
            new_job_finish_time = job_processing_time + next_thread.finish_time
            results.append(ThreadJob(thread_id=next_thread.thread_id, start_time=next_thread.finish_time, finish_time=new_job_finish_time))
            tj = ThreadJob(thread_id=next_thread.thread_id,start_time=None,finish_time=new_job_finish_time)
            self.thread_heap.insert(tj)
        return results
