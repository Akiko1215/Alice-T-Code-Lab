import cupy as cp
import numpy as np
import time
import math

"""
Armstrong Numbers
Zähle die Anzahl der Stellen $k$ der Zahl.
Erbebe jede einzelne Ziffer in die $k$-te Potenz.
Addiere diese Werte.
Wenn das Ergebnis der ursprünglichen Zahl entspricht, ist es eine Armstrong-Zahl.
"""

#String Variante
def check_armstrong_number(num: int) -> tuple[bool, int]:
    #Zähle die Anzahl der Stellen $k$ der Zahl.
    num_str = str(num)
    num_length = len(num_str)

    #Erbebe jede einzelne Ziffer in die $k$-te Potenz.
    
    int_list = [int(c) for c in num_str]
   
    total = sum([i**num_length for i in int_list])

    return total == num, total

#Mathe Log10 Variante   
def check_math_armstrong_number(num: int):

    if num <= 0:
        return False, 0

    temp_num = num
    num_length = math.floor(math.log10(num)) + 1  
    int_list = []
    
    while temp_num > 0:
        int_list.append(temp_num % 10)
        temp_num = temp_num // 10

    total =  sum(i**num_length for i in int_list)

    return total == num, total

#Numpy Vektorisierung
def armstrong_numpy(limit):
    nums = np.arange(1, limit, dtype=np.int64)

    digits = np.floor(np.log10(nums)).astype(int) + 1

    total_sums = np.zeros_like(nums, dtype=np.int64)

    temp_nums = nums.copy()

    for _ in range(np.max(digits)):
        digits_at_pos = temp_nums % 10
        total_sums += np.power(digits_at_pos, digits)
        temp_nums //= 10

    results = nums[total_sums == nums]
    return results


def benchmark_py(limit):
    start = time.time()
    arm_list = [i for i in (range(1, limit)) if check_math_armstrong_number(i)[0] == True]
    end = time.time() 
    print(f"Mathe-Variante:  {end - start:.4f} Sekunden")

    start = time.time()
    arm_list = [i for i in (range(1, limit)) if check_armstrong_number(i)[0] == True]
    end = time.time() 
    print(f"String-Variante:  {end - start:.4f} Sekunden")

def benchmark_numpy(limit):
    start = time.time()
    found = armstrong_numpy(limit)
    print(f"Gefunden: {found}")
    print(f"NumPy-Dauer: {time.time() - start:.4f} Sekunden")

#Check ob Cupy Hardware korrekt erkennt
def cupy_test():
    # Informationen zur GPU ausgeben
    device = cp.cuda.Device(0)
    print(f"Grafikkarte gefunden: {device.attributes['MultiProcessorCount']} SMs auf {cp.cuda.runtime.getDeviceProperties(0)['name'].decode()}")

    # Ein kleiner Test-Vektor auf der GPU
    x_gpu = cp.array([1, 2, 3])
    print(f"Test-Array auf GPU: {x_gpu}")

#Performance Test auf CPU und GPU
def compare_performance(limit):
    # --- NUMPY (CPU: Ryzen 7600X3D) ---
    start_cpu = time.time()
    nums_cpu = np.arange(1, limit, dtype=np.int64)
    digits_cpu = np.floor(np.log10(nums_cpu)).astype(np.int64) + 1
    sums_cpu = np.zeros_like(nums_cpu, dtype=np.int64)
    temp_cpu = nums_cpu.copy()
    
    for _ in range(int(np.max(digits_cpu))):
        sums_cpu += np.power(temp_cpu % 10, digits_cpu)
        temp_cpu //= 10
    
    res_cpu = nums_cpu[sums_cpu == nums_cpu]
    duration_cpu = time.time() - start_cpu
    

    # --- CUPY (GPU: RTX 4070 Super) ---
    # Wir machen einen "Warm-up" Run, damit CuPy die Kernel kompilieren kann
    _ = cp.arange(10, dtype=cp.int64) 
    
    start_gpu = time.time()
    nums_gpu = cp.arange(1, limit, dtype=np.int64)
    digits_gpu = cp.floor(cp.log10(nums_gpu)).astype(cp.int64) + 1
    sums_gpu = cp.zeros_like(nums_gpu, dtype=cp.int64)
    temp_gpu = nums_gpu.copy()
    
    for _ in range(int(cp.max(digits_gpu))):
        sums_gpu += cp.power(temp_gpu % 10, digits_gpu)
        temp_gpu //= 10
        
    # Warten, bis die GPU wirklich fertig ist (Synchronisation)
    cp.cuda.Stream.null.synchronize() 
    res_gpu = nums_gpu[sums_gpu == nums_gpu].get() # .get() holt Ergebnis zum PC zurück
    duration_gpu = time.time() - start_gpu

    print(f"Limit: {limit:,}")
    print(f"CPU (NumPy): {duration_cpu:.4f}s")
    print(f"GPU (CuPy):  {duration_gpu:.4f}s")
    print(f"Gefunden: {res_gpu}")

# Starte das Duell!
compare_performance(100_000_000)





