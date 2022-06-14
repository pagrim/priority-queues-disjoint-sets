import heapq
import re
import sys

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
        self.thread_heap = [ThreadJob(thread_id=i, start_time=None, finish_time=0) for i in range(num_threads)]
        heapq.heapify(self.thread_heap)

    def process(self):
        results = []
        while len(self.jobs) > 0:
            job_processing_time = self.jobs.pop(0)
            next_thread = heapq.heappop(self.thread_heap)
            new_job_finish_time = job_processing_time + next_thread.finish_time
            results.append(ThreadJob(thread_id=next_thread.thread_id, start_time=next_thread.finish_time, finish_time=new_job_finish_time))
            tj = ThreadJob(thread_id=next_thread.thread_id,start_time=None,finish_time=new_job_finish_time)
            heapq.heappush(self.thread_heap, tj)
        return results


if __name__ == '__main__':
    match_object = re.match(r'(\d+)\s(\d+)', sys.stdin.readline().rstrip())
    num_threads, num_jobs = int(match_object.group(1)), int(match_object.group(2))
    jobs = [int(jb) for jb in sys.stdin.readline().rstrip().split(" ")]
    pp = ParallelProcessor(jobs=jobs, num_threads=num_threads)
    results = pp.process()
    for tj in results:
        print(f"{tj.thread_id} {tj.start_time}")

