import math

# C: Execution time (WCET), T: Period and relative deadline
tasks = [
    {'id': 1, 'C': 2.4084, 'T': 10},
    {'id': 2, 'C': 3, 'T': 10},
    {'id': 3, 'C': 2, 'T': 20},
    {'id': 4, 'C': 2, 'T': 20},
    {'id': 5, 'C': 2, 'T': 40},
    {'id': 6, 'C': 2, 'T': 40},
    {'id': 7, 'C': 3, 'T': 80},
]


current_time = 0
total_waiting_time = 0
hyper_period = 80 # Hyperperiod is the Least Common Multiple (LCM) of all T
jobs = []

# Create all job instances 
for t in tasks:
    num_instances = hyper_period // t['T']
    for i in range(num_instances):
        jobs.append({
            'id': t['id'],
            'name': f"J{t['id']},{i+1}",
            'release': i * t['T'], # Arrival time of the job
            'C': t['C'],           # Worst Case Execution Time
            'deadline': (i + 1) * t['T'], # Absolute deadline
            'completed': False
        })

# Table Header for the report
print(f"{'Start':<8} | {'Job':<8} | {'End':<8} | {'DL':<5} | {'R.Time':<7} | {'Status'}")
print("-" * 65)

#Non-preemptive EDF but T5 can miss a deadline
while any(not j['completed'] for j in jobs):
    # Identify all jobs that have arrived and are not yet finished
    ready_jobs = [j for j in jobs if j['release'] <= current_time and not j['completed']]
    
    if not ready_jobs:
        # If no jobs are ready, pass to the next job arrival time to maximize idle time efficiency
        current_time = min(j['release'] for j in jobs if not j['completed'])
        continue

    # optimized part : Minimize total waiting time while only allowing T5 to miss deadlines
    best_job = None
    min_priority_val = (float('inf'), float('inf'))
    
    for j in ready_jobs:
        # To minimize wait for others, we assign a virtual very late deadline to T5 
        # This pushes T5 to the end of the ready queue
        p_deadline = 9999 if j['id'] == 5 else j['deadline']
        
        # EDF Priority Selection: 
        # 1. Earliest absolute deadline
        # 2. Shortest execution time (C) in case of equality
        current_val = (p_deadline, j['C'])
        
        if current_val < min_priority_val:
            min_priority_val = current_val
            best_job = j

    # Calculate performance 
    wait = current_time - best_job['release']
    total_waiting_time = total_waiting_time + wait
    finish_time = current_time + best_job['C']
    response_time = finish_time - best_job['release']  # Response Time (R.Time) is the time from release to completion
    
    # Check if the deadline was met 
    is_ok = finish_time <= (best_job['deadline'] + 0.0001) 
    if is_ok:
        status = "OK"
    elif best_job['id'] == 5:
        status = "MISS BUT IT'S OK"        # Authorized deadline miss for task T5 
    else:
        status = "CRITICAL"    # Unauthorized deadline miss for other tasks

     # Print job execution details
    print(f"t={round(current_time, 4):<6} | {best_job['name']:<8} | {round(finish_time, 4):<8} | {best_job['deadline']:<5} | {round(response_time, 4):<7} | {status}")
    
    current_time = finish_time
    best_job['completed'] = True


print("-" * 65)
print(f"TOTAL WAITING TIME : {round(total_waiting_time, 4)}")
print(f"Total Processor Idle Time : {round(hyper_period - sum(j['C'] for j in jobs), 4)}")

