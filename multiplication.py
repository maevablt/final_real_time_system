import random
import time 
import numpy as np
def multiplication():
    a = random.getrandbits(int(2E4))
    b = random.getrandbits(int(2E4))
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

q1, q2, q3 = np.percentile(execution_time, [25, 50, 75])

print("Minimum",minimum)
print("Maximum (WECT)",maximum)
print("Q1",q1)
print("Q2",q2)
print("Q3",q3)