from timer import time_function
from screening import virtual_screening, get_pharmacophore

def main():
    dataset_path = "/home/daniel/Documents/MyNotebooks/zinc/data/shards"
    _, rdkit_pharmacophore = get_pharmacophore()
    sort = True
    
    n_runs = 7
    avg_time = time_function(virtual_screening, args=(dataset_path, rdkit_pharmacophore, sort), 
                             n_runs=n_runs, verbose=True)
    print(f"Avg time: {avg_time} for {n_runs} runs.")
    
    with open("./time.txt", "w") as fp:
        fp.write(f"Avg time: {avg_time} for {n_runs} runs.")
    
# Avg time: 0:09:18.836393

if __name__=="__main__":
   main()