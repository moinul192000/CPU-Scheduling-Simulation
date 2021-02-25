# Class "Process" represents an individual Process
class Process:
    def __init__(self, id, at, bt, p):
        self.id              = id  # Process ID
        self.priority        = p # priority
        self.completed       = 0  # 0 - not completed , 1 - completed
        self.wait_time       = 0  # Waiting Time
        self.burst_time      = bt  # Burst Time
        self.arrival_time    = at  # Arrival Time
        self.remaining_time  = bt  # Remaining time
        self.completion_time = 0  # when a process was completed
        self.turnaround_time = 0  # Turn Around Time

    def __str__(self):
        return "{: >15} {: >15} {: >15} {: >15} {: >15} {: >15} {: >15}".format(
            self.id, self.arrival_time, self.priority, self.burst_time, self.completion_time, 
            self.turnaround_time, self.wait_time)

#Non Preemptive priority scheduling
def non_preemptive_priority(pros, size):
    print("\n        >>>>>>>>>>>>>>>>>>>> Non Preemptive Priority Scheduling <<<<<<<<<<<<<<<<<<<\n\n")
    current_time, process_execution_seq = 0, []
    for process in pros:
        ready_q, temp_q, temp_process = [], [], None
        for p in pros:
            if (p.arrival_time <= current_time) and not p.completed:
                ready_q.append(p)
            elif not p.completed:
                temp_q.append(p)
        if ready_q:
            ready_q.sort(key=lambda p: p.priority)
            current_time += ready_q[0].burst_time
            temp_process = list(filter(lambda p: p.id == ready_q[0].id, pros))[0]
        else:
            if current_time < temp_q[0].arrival_time:
                current_time = temp_q[0].arrival_time
            current_time += temp_q[0].burst_time
            temp_process = list(filter(lambda p: p.id == temp_q[0].id, pros))[0]
        temp_process.completed, temp_process.completion_time = 1, current_time
        process_execution_seq.append(temp_process.id)
        calculate_wait_turnaround_times(temp_process)
    print_results(pros, size, process_execution_seq)


# Simulate SJF with preemption scheduling
def preemptive_sjf(pros, size):
    print("\n        >>>>>>>>>>>>>>>>>>>> SJF Preemptive Scheduling <<<<<<<<<<<<<<<<<<<\n\n")
    current_time, process_execution_seq = 0, []
    while True:
        ready_q, temp_q, temp_process = [], [], None
        for process in pros:
            if process.arrival_time <= current_time and not process.completed:
                ready_q.append(process)
            elif not process.completed:
                temp_q.append(process)
        if not ready_q and not temp_q: break            
        if ready_q:
            ready_q.sort(key=lambda p: p.remaining_time)
            current_time += 1
            process_execution_seq.append(ready_q[0].id)
            temp_process = list(filter(lambda p: p.id == ready_q[0].id, pros))[0]
        else:
            if current_time < temp_q[0].remaining_time:
                current_time = temp_q[0].remaining_time
            current_time += 1
            process_execution_seq.append(temp_q[0].id)
            temp_process = list(filter(lambda p: p.id == temp_q[0].id, pros))[0]
        temp_process.remaining_time -= 1
        if not temp_process.remaining_time:  #If remaining Burst Time of a process is 0, it means the process is completed
            temp_process.completed =1
            temp_process.completion_time = current_time
            calculate_wait_turnaround_times(temp_process)
    print_results(pros, size, process_execution_seq)

# Simulate SJF without preemption scheduling
def non_preemptive_sjf(pros, size):
    current_time, minm, flag, done, process_execution_seq = 0, 999999999, False, 0, []
    print("\n        >>>>>>>>>>>>>>>>>>>> SJF Non Preemptive Scheduling <<<<<<<<<<<<<<<<<<<\n\n")
    while done != size:
        for process in pros:
            if process.arrival_time <= current_time and process.completed == 0 and process.burst_time < minm:
                flag, minm, cur_process = True, process.burst_time, process
        if flag: 
            current_time += cur_process.burst_time
            cur_process.completion_time, cur_process.completed = current_time, 1
            calculate_wait_turnaround_times(cur_process)
            process_execution_seq.append(cur_process.id)
            done += 1
            flag, minm = False, 999999999
        else:
            current_time += 1
    print_results(pros, size, process_execution_seq)

# Simulates Round-Robin Schdeuling
def round_robin(pros, size, q):
    print("\n        >>>>>>>>>>>>>>>>>>>> Round Robin Scheduling <<<<<<<<<<<<<<<<<<<\n\n")
    process_execution_seq, ready_q, current_time = [],[], 0
    while True:
        temp_q = []
        for i in range(size):
            temp_process = None
            if pros[i].arrival_time <= current_time and not pros[i].completed:
                found = False
                if ready_q:
                    found = any(r.id == pros[i].id for r in ready_q)
                if not found:
                    ready_q.append(pros[i])
                if ready_q and process_execution_seq:
                    for j in range(len(ready_q)):
                        if ready_q[j].id == process_execution_seq[-1]:
                            ready_q.insert((len(ready_q) - 1), ready_q.pop(j))
            elif not pros[i].completed:
                temp_q.append(pros[i])
        if not ready_q and not temp_q: break
        if ready_q:
            if ready_q[0].remaining_time > q:
                current_time += q
                process_execution_seq.append(ready_q[0].id)
                temp_process = list(filter(lambda p: p.id == ready_q[0].id, pros))[0]
                temp_process.remaining_time -= q
                ready_q.pop(0)
            elif ready_q[0].remaining_time <= q:
                current_time += ready_q[0].remaining_time
                process_execution_seq.append(ready_q[0].id)
                temp_process = list(filter(lambda p: p.id == ready_q[0].id, pros))[0]
                temp_process.remaining_time, temp_process.completed, temp_process.completion_time = 0, 1, current_time
                calculate_wait_turnaround_times(temp_process)
                ready_q.pop(0)
        else:
            if current_time < temp_q[0].arrival_time:
                current_time = temp_q[0].arrival_time
            if temp_q[0].remaining_time > q:
                current_time += q
                process_execution_seq.append(temp_q[0].id)
                temp_process = list(filter(lambda p: p.id == temp_q[0].id, pros))[0]
                temp_process.remaining_time -= q
            elif temp_q[0].remaining_time <= q:
                current_time += temp_q[0].remaining_time
                process_execution_seq.append(temp_q[0].id)
                temp_process = list(filter(lambda p: p.id == temp_q[0].id, pros))[0]
                temp_process.remaining_time, temp_process.completed, temp_process.completion_time = 0, 1, current_time
                calculate_wait_turnaround_times(temp_process)

    print_results(pros, size, process_execution_seq)

def preemptive_priority(pros, size):
    print("\n        >>>>>>>>>>>>>>>>>>>> Priority Preemptive Scheduling <<<<<<<<<<<<<<<<<<<\n\n")
    current_time, process_execution_seq = 0, []
    while True:
        ready_q, temp_q, temp_process = [], [], None
        for p in pros:
            if (p.arrival_time <= current_time) and not p.completed:
                ready_q.append(p)
            elif not p.completed:
                temp_q.append(p)
        if not ready_q and not temp_q: break
        if ready_q:
            ready_q.sort(key=lambda p: p.priority)
            current_time += 1
            process_execution_seq.append(ready_q[0].id)
            temp_process = list(filter(lambda p: p.id == ready_q[0].id, pros))[0]
        else:
            temp_q.sort(key=lambda p: p.arrival_time)
            if current_time < temp_q[0].arrival_time:
                current_time = temp_q[0].arrival_time
            current_time += 1
            process_execution_seq.append(temp_q[0].id)
            temp_process = list(filter(lambda p: p.id == temp_q[0].id, pros))[0]
        temp_process.remaining_time -= 1
        if temp_process.remaining_time <= 0:
            temp_process.completed, temp_process.completion_time = 1, current_time
        calculate_wait_turnaround_times(temp_process)
    print_results(pros, size, process_execution_seq)


def calculate_wait_turnaround_times(process):
    process.turnaround_time = process.completion_time - process.arrival_time
    process.wait_time = process.turnaround_time - process.burst_time
    if process.wait_time < 0:
        process.wait_time = 0


def print_results(pros, size, sequence):
    sequence = [v for i, v in enumerate(sequence) if i == 0 or v != sequence[i-1]]
    pros = sorted(pros, key=lambda p: p.id)
    print("{: >15} {: >15} {: >15} {: >15} {: >18} {: >18} {: >15}".format("Process ID", "Arrival Time", "Burst Time", "Priority", "Completion Time", "Turnaround Time", "Waiting Time"))
    print("\n".join(str(p) for p in pros))
    print(f"\nAverage Waiting time    : {round(sum(p.wait_time for p in pros) / size, 2)}")
    print(f"Average Turnaround time : {round(sum(p.turnaround_time for p in pros) / size, 2)}")
    print("Process Execution Queue "+ " -> ".join(p for p in sequence) +"\n")
    reset_process_data(pros)

def reset_process_data(pros):
    for process in pros:
        process.completed, process.remaining_time = 0, process.burst_time

def start_simulation(pros, quantum, size):
    non_preemptive_sjf(pros, size)
    preemptive_sjf(pros, size)
    non_preemptive_priority(pros, size)
    preemptive_priority(pros, size)
    round_robin(pros, size, quantum)

def get_process_data(no_of_processes):
    pros = []
    for i in range(no_of_processes):
        id = f"P{i}"
        arrival_time = int(input(f"\nPlease enter Arrival Time for '{id}': "))
        priority = int(input(f"Please enter Priority for '{id}': "))
        burst_time = int(input(f"Please enter Burst Time for '{id}': "))
        pros.append(Process(id, arrival_time, burst_time, priority))
    quantum = int(input("Please enter Time Quantum (Default 3) : ") or "3")
    return (pros, quantum)

def print_menu():       # Your menu design here
        print(10 * "-", "Select Algorithm", 10 * "-")
        print("1. Round Robin ")
        print("2. Preemptive SJF")
        print("3. Non-Preemptive SJF ")
        print("4. Preemptive Priority ")        
        print("5. Non-Preemptive Priority ")
        print("6. All ")
        print("7. Exit")
        

if __name__ == "__main__":
    print("=============================================")
    print("\n")
    print("\t TSN2101 - Operating System")
    print("\t Assignment ")
    print("\t Simulation of \n\t CPU Scheduling Algorithm")
    print("\n")
    print("==============================================")
    print("Note: Lower Priority value means Higher Priority")
    no_of_processes = int(input("Enter total number of processes (3 to 10) : "))
    loop = True
    if 2 < no_of_processes < 11:
        pros, quantum = get_process_data(no_of_processes)

        #test date
        # pros, quantum = [], 3
        # pros.append(Process("P0", 0, 8, 2))
        # pros.append(Process("P5", 0, 6, 1))
        # pros.append(Process("P1", 4, 15, 5))
        # pros.append(Process("P4", 9, 13, 4))
        # pros.append(Process("P2", 7, 9, 3))
        # pros.append(Process("P3", 13, 5, 1))

        # sorting processes on basis of their arrival time
        pros = sorted(pros, key=lambda p: p.arrival_time)
        print_menu()
        while loop:          # While loop which will keep going until loop = False
            choice = input("Enter your choice [1-7]: ")

            if choice == '1':
                round_robin(pros, size, quantum)
                loop = False
            elif choice == '2':
                preemptive_sjf(pros, size)
                loop = False
            elif choice == '3':
                non_preemptive_sjf(pros, size)
                loop = False
            elif choice == '4':
                preemptive_priority(pros, size)
                loop = False
            elif choice == '5':
                non_preemptive_priority(pros, size)
                loop = False
            elif choice == '6':
                start_simulation(pros, quantum, no_of_processes)
                loop = False
            elif choice == '7':
                print("Exiting..")
                loop = False  # This will make the while loop to end
            else:
                # Any inputs other than values 1-4 we print an error message
                input("Wrong menu selection. Enter any key to try again..")
        
    else:
        print("Number of processes can range from 3 and 10. Try again.")

