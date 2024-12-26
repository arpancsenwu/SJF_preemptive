class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid                # Process ID
        self.arrival_time = arrival_time  # Arrival Time
        self.burst_time = burst_time  # Burst Time
        self.remaining_time = burst_time  # Remaining Time
        self.completion_time = 0      # Completion Time
        self.turnaround_time = 0      # Turnaround Time
        self.waiting_time = 0         # Waiting Time
        self.start_time = -1          # Start Time
        self.response_time = -1       # Response Time (initially -1 to indicate not yet started)

def sjf_preemptive(processes):
    n = len(processes)
    time = 0
    completed = 0
    min_burst_time = float('inf')
    shortest_job = None
    check = False

    while completed != n:
        # Find the process with the smallest remaining time at the current time
        for i in range(n):
            if processes[i].arrival_time <= time and processes[i].remaining_time > 0:
                if processes[i].remaining_time < min_burst_time:
                    min_burst_time = processes[i].remaining_time
                    shortest_job = i
                    check = True
                elif processes[i].remaining_time == min_burst_time:
                    # If two processes have the same burst time, choose the one that arrived first
                    if processes[i].arrival_time < processes[shortest_job].arrival_time:
                        shortest_job = i

        if not check:
            time += 1
            continue

        # Record the response time if this is the first time the process gets the CPU
        if processes[shortest_job].response_time == -1:
            processes[shortest_job].response_time = time - processes[shortest_job].arrival_time

        # If this is the first time the process is getting the CPU, record the start time
        if processes[shortest_job].start_time == -1:
            processes[shortest_job].start_time = time

        # Process the shortest job
        processes[shortest_job].remaining_time -= 1
        min_burst_time = processes[shortest_job].remaining_time

        # If the process is complete
        if processes[shortest_job].remaining_time == 0:
            completed += 1
            min_burst_time = float('inf')
            check = False

            # Record the completion time of the process
            processes[shortest_job].completion_time = time + 1
            processes[shortest_job].turnaround_time = processes[shortest_job].completion_time - processes[shortest_job].arrival_time
            processes[shortest_job].waiting_time = processes[shortest_job].turnaround_time - processes[shortest_job].burst_time

        time += 1

    return processes

# Helper function to print the results
def print_process_info(processes):
    print("\nPID\tArrival Time\tBurst Time\tCompletion Time\tTurnaround Time\tWaiting Time\tResponse Time")
    total_tat = 0
    total_wt = 0
    total_rt = 0
    for process in processes:
        total_tat += process.turnaround_time
        total_wt += process.waiting_time
        total_rt += process.response_time
        print(f"{process.pid}\t{process.arrival_time}\t\t{process.burst_time}\t\t{process.completion_time}\t\t{process.turnaround_time}\t\t{process.waiting_time}\t\t{process.response_time}")
    
    print(f"\nAverage Turnaround Time: {total_tat / len(processes):.2f}")
    print(f"Average Waiting Time: {total_wt / len(processes):.2f}")
    print(f"Average Response Time: {total_rt / len(processes):.2f}")

# Function to take user input for processes
def input_processes():
    n = int(input("Enter the number of processes: "))
    processes = []
    for i in range(n):
        print(f"\nProcess {i + 1}:")
        arrival_time = int(input(f"Enter Arrival Time for Process {i + 1}: "))
        burst_time = int(input(f"Enter Burst Time for Process {i + 1}: "))
        processes.append(Process(i + 1, arrival_time, burst_time))
    return processes

# Main function to run the scheduler
if __name__ == "__main__":
    processes = input_processes()
    completed_processes = sjf_preemptive(processes)
    print_process_info(completed_processes)
