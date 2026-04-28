import random
import time 
import statistics
def multiplication():
    a = random.getrandbits(int(1E4))
    b = random.getrandbits(int(1E4))
    start = time.perf_counter()
    c = a * b
    end = time.perf_counter()
    r_time = end - start
    return r_time

execution_time = []
for i in range(1000):
    t = multiplication()*1000
    execution_time.append(t)

minimum = min(execution_time)
maximum = max(execution_time)
Q = statistics.quantiles(execution_time, n=4)



print("Minimum",minimum)
print("Maximum (WECT)",maximum)
print("Q1",Q[0])
print("Q2 ",Q[1])
print("Q3" ,Q[2])