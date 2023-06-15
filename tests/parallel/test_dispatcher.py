from mlserver.parallel.dispatcher import Dispatcher


async def test_on_worker_stop(dispatcher: Dispatcher):
    worker = list(dispatcher._workers.values())[0]
    await worker.stop()
    dispatcher.on_worker_stop(worker)

    assert worker.pid not in dispatcher._workers
    # Ensure worker is no longer in round robin rotation
    workers_count = len(dispatcher._workers)
    for _ in range(workers_count + 1):
        worker_pid = next(dispatcher._workers_round_robin)
        assert worker_pid != worker.pid
