import pytest

from parallel_processor import ParallelProcessor, ThreadJob


def test_less_than():
    tj1 = ThreadJob(*(0, None, 1))
    tj2 = ThreadJob(*(0, None, 2))
    tj3 = ThreadJob(*(1, None, 1))
    assert tj1 < tj2 and tj1 < tj3 and tj3 < tj2


@pytest.mark.parametrize(("jobs", "num_threads", "exp_ids_starts"), [
    ([1, 2, 3, 4, 5], 2, [(0, 0), (1, 0), (0, 1), (1, 2), (0, 4)]),
    ([1] * 20, 4,
     [(id, start) for start_range in [[(0, i), (1, i), (2, i), (3, i)] for i in range(5)] for id, start in start_range])
])
def test_process(jobs, num_threads, exp_ids_starts):
    pp = ParallelProcessor(jobs=jobs, num_threads=num_threads)
    exp_res = [ThreadJob(thread_id=id, start_time=start, finish_time=None) for id, start in exp_ids_starts]
    res = pp.process()
    assert res == exp_res
