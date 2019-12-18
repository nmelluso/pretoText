from joblib import delayed, Parallel
from tqdm import tqdm


SOFT = 1  # parallelism by multithreading
HARD = 2  # parallelism by multiprocessing
HARD_SMART = 3  # parallelism by loky


class WorkersPool(Parallel):
    """
    An optimized :class:`joblib.Parallel` class for performing parallelized tasks.
    It is made easier to select the parallelisation level and the size of the pool.
    
    """

    def __init__(self, level=SOFT, size=-1, verbose=False):
        if level == SOFT:
            backend = "threading"
        elif level == HARD:
            backend = "multiprocessing"
        elif level == HARD_SMART:
            backend = "loky"

        super(WorkersPool, self).__init__(
            n_jobs=size,
            backend=backend,
            require="sharedmem" if level == SOFT else None,
            verbose=100 if verbose else 0,
        )

    def perform_job(self, items, task, *task_args, **task_kwargs):
        """
        Perform a task to each element of a set of items in parallel.
        
        Args:
            items (list): 
                A set of elements which to perform a task to.
            task (function): 
                A function which will be applied to each element.
        
        Returns:
            list: 
                Contains any returned output from each task performed.
        """
        return self(
            delayed(task)(item, *task_args, **task_kwargs) for item in tqdm(items)
        )


def hire(level=SOFT, n_workers=-1, verbose=False):
    """
    Get a :class:`WorkersPool` with a number of ``n_workers`` ready for a job.
    
    Args:
        level (int, optional): 
            The level of parallalisation: 1 for *multithreading*, 2 for *multiprocessing*. 
            Defaults to SOFT.
        n_workers (int, optional): 
            The number of workers that will work simultaneously. 
            If ``level`` is ``SOFT``, the best value is the max number of threads supported by the CPU.
            If ``level`` is ``HARD``, the best value is the number of cores the CPU has.
            Defaults to -1 (automatically get *cores count* workers).
        verbose (bool, optional): 
            Activate a verbosity. It gives progress visual feedbacks. 
            Defaults to False.
    
    Returns:
        WorkersPool: The :class:`WorkerPool` ready for a job.
    """
    return WorkersPool(level=level, size=n_workers, verbose=verbose)


def perform_job(
    items, task, level=SOFT, n_workers=-1, verbose=False, *task_args, **task_kwargs
):
    """
    Perform a task to each element of a set of items in parallel.
    
    Args:
        items (list): 
            A set of elements which to perform a task to.
        task (function): 
            A function which will be applied to each element.
        level (int, optional): 
            The level of parallalisation: 1 for *multithreading*, 2 for *multiprocessing*. 
            Defaults to SOFT.
        n_workers (int, optional): 
            The number of workers that will work simultaneously. 
            If ``level`` is ``SOFT``, the best value is the max number of threads supported by the CPU.
            If ``level`` is ``HARD``, the best value is the number of cores the CPU has.
            Defaults to -1 (automatically get *cores count* workers).
        verbose (bool, optional): 
            Activate a verbosity. It gives progress visual feedbacks. 
            Defaults to False.
    
    Returns:
        list: 
            Contains any returned output from each task performed.
    """
    pool = hire(level=level, n_workers=n_workers, verbose=verbose)
    return pool.perform_job(items, task, *task_args, **task_kwargs)
