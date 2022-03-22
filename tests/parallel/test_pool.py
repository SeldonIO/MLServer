import os

from mlserver.parallel.pool import InferencePool


def check_pid(pid):
    """
    Check For the existence of a unix pid.

    From https://stackoverflow.com/a/568285/5015573
    """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def test_pool(pool: InferencePool):
    # TODO: Read number of workers from settings
    assert len(pool._workers) == 4

    for worker_pid in pool._workers:
        assert check_pid(worker_pid)


async def test_close(pool: InferencePool):
    worker_pids = [pid for pid in pool._workers]

    await pool.close()

    assert len(pool._workers) == 0
    for worker_pid in worker_pids:
        assert not check_pid(worker_pid)
