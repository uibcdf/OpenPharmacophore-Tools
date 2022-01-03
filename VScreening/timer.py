import time
import datetime

def time_function(function, args, n_runs=7, verbose=False):
    
    runs = []
    for ii in range(n_runs):
        startt = time.time()
        function(*args)
        endt = time.time()
        runs.append(endt - startt)
        if verbose:
            print(f"Finished run {ii}/{n_runs}")
        
    assert len(runs) == n_runs
    avg_time = sum(runs) / len(runs)
    
    return datetime.timedelta(seconds=avg_time)