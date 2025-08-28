def get_integer_processes(number):
    while True:
        try:
            number = int(number)
            if number >= 0:
              return number
            else:
              number = input("Please enter an integer greater than or equal to 0. ")
        except ValueError:
            number = input("That's not a valid integer! Please try again.")

def get_integer(number):
    while True:
        try:
            number = int(number)
            if number > 0:
              return number
            else:
              number = input("Please enter an integer greater than 0. ")
        except ValueError:
            number = input("That's not a valid integer! Please try again.")

def get_integer_algorithm_select(number):
    while True:
        try:
            number = int(number)
            if 1 <= number <= 5:
              return number
            else:
              number = input("Please enter an integer from 1 to 5. ")
        except ValueError:
            number = input("That's not a valid integer! Please try again.")


def gnatt(array):


    print(end="|")

    for i in array:

        print(f"{i[0]:^{2*i[2]}}", end="|")

    print("")

    print(end="|")

    for j in array:

        print(f"{j[4]:^{2*j[2]}}", end="|")

def gnatt_preemptive(array):


    print(end="|")

    for i in array:

        print(f"{i[0]:^{2*i[8]}}", end="|")

    print("")

    print(end="|")

    for j in array:

        print(f"{j[4]:^{2*j[8]}}", end="|")


def get_data(array):
    process_number = get_integer(input("Please enter how many processes to run. "))
    for i in range(process_number):                 # Creating the table of details
        process_name = "P" + str(i + 1)
        process_arrival_time = get_integer_processes((input("Please enter the arrival time for " + str(process_name) + " ")))
        process_burst_time = get_integer_processes(input("Please enter the burst time for " + str(process_name) + " "))
        process_priority = get_integer_processes(input("Please enter the priority for " + str(process_name) + " "))
        process_completion_time = 0
        process_response_time = 0
        process_waiting_time = 0
        process_turnaround_time = 0
        process_details = [process_name, process_arrival_time, process_burst_time, process_priority,
                           process_completion_time, process_response_time, process_waiting_time,
                           process_turnaround_time]
        array.append(process_details)

    return array


""" element [0] = name
    element [1] = arrival time
    element [2] = burst time
    element [3] = priority 
    element [4] = completion time 
    element [5] = response time
    element [6] = waiting time
    element [7] = turnaround time"""


def sort_by_arrival(array):
    return sorted(array, key=lambda process: process[1])

def sort_by_burst_time(array):
    return sorted(array, key=lambda process: process[2])

def sort_by_priority(array):
    return sorted(array, key=lambda process: process[3])

def first_come_first_serve(array):
    result_array = []   #Creating results array for Gnatt to print from
    array = sort_by_arrival(array)    # sort by arrival first
    time = 0 # this captures time overall
    remaining_processes = array.copy()    # copy array to work in

    while remaining_processes:
        arrived_processes = [p for p in remaining_processes if p[1] <= time] #this creates an array of processes that have arrived with current time
        if arrived_processes:
            current_process = arrived_processes.pop(0) # pull the first available process
            current_process[5] = time - current_process[1]  # response time
            time += current_process[2] # execute what is available (non-preemptive)
            current_process[4] = time # completion time
            current_process[7] = current_process[4] - current_process[1] # waiting time
            current_process[6] = current_process[7] - current_process[2] # turnaround time
            result_array.append(current_process)    # print to results array
            remaining_processes.remove(current_process)    # remove from remaining processes
        else:
            time += 1

    return result_array

def shortest_process_next(array):
    result_array = []
    array = sort_by_arrival(array)
    time = 0
    remaining_processes = array.copy()

    while remaining_processes:
        arrived_processes = [p for p in remaining_processes if p[1] <= time]
        if arrived_processes:
            arrived_processes = sort_by_burst_time(arrived_processes)       # sort by burst time from the available processes
            current_process = arrived_processes.pop(0)  # pull the first available process
            current_process[5] = time - current_process[1]  # response time
            time += current_process[2]  # execute what is available (non-preemptive)
            current_process[4] = time  # completion time
            current_process[7] = current_process[4] - current_process[1]  # waiting time
            current_process[6] = current_process[7] - current_process[2]  # turnaround time
            result_array.append(current_process)
            remaining_processes.remove(current_process)
        else:
            time += 1

    return result_array



def shortest_remaining_time(array):
    result_array = []
    array = sort_by_arrival(array)
    time = 0
    remaining_processes = array.copy()
    ready_que = []

    for process in remaining_processes:         # adding another element for preemptive algorithims to track original burst time. this is used for the calculating the wait time
        process.append(process[2])

    while remaining_processes or ready_que:  # either one of the arrays will be active, which keeps this loop going.
        arrived_processes = [p for p in remaining_processes if p[1] <= time]
        for process in arrived_processes:   # if there are arrived processes, add them to the ready que and remove from remaining processes
            ready_que.append(process)
            remaining_processes.remove(process)
        if ready_que:
            ready_que = sort_by_burst_time(ready_que)
            current_process = ready_que.pop(0)
            if current_process[5] == 0:             # checks if the response time has not been set
                current_process[5] = time - current_process[1]  # response time = current time - arrival time
            current_process[2] -= 1
            time += 1
            if current_process[2] == 0:
                current_process[4] = time
                current_process[7] = current_process[4] - current_process[1] # calculate turn around time
                current_process[6] = current_process[7] - current_process[8] # calculate wait time
                result_array.append(current_process)

            else:
                ready_que.append(current_process) # if the process did not finish, then it goes back to the ready que after 1 unit of execution.
        else:
            time += 1

    return result_array



def round_robin(array, time_q):
    result_array = []
    array = sort_by_arrival(array)  # Sort by arrival time
    time = 0
    remaining_processes = array.copy()
    ready_que = []

    for process in remaining_processes:         # adding another element for preemptive algorithims to track original burst time. this is used for the calculating the wait time
        process.append(process[2])

    while remaining_processes or ready_que:
        arrived_processes = [p for p in remaining_processes if p[1] <= time]
        for process in arrived_processes:   # if there are arrived processes, add them to the ready que and remove from remaining processes
            ready_que.append(process)
            remaining_processes.remove(process)
        if ready_que:
            current_process = ready_que.pop(0)
            if current_process[5] == 0:             # checks if the response time has not been set
                current_process[5] = time - current_process[1]  # response time = current time - arrival time
            time_slice = min(current_process[2], time_q)  # uses whatever is smaller, the time_slice or the remaining execution time.
            current_process[2] -= time_slice
            time += time_slice
            if current_process[2] ==0:
                current_process[4] = time
                current_process[7] = current_process[4] - current_process[1]  # calculate turn around time
                current_process[6] = current_process[7] - current_process[8]  # calculate wait time
                result_array.append(current_process)
            else:
                ready_que.append(current_process)
        else:
            time += 1

    return result_array



def priority_scheduling(array):
    result_array = []
    array = sort_by_arrival(array)
    time = 0
    remaining_processes = array.copy()

    while remaining_processes:
        arrived_processes = [p for p in remaining_processes if p[1] <= time] #this creates an array of processes that have arrived with current time
        if arrived_processes:
            arrived_processes = sort_by_priority(arrived_processes)
            current_process = arrived_processes.pop(0)
            current_process[5] = time - current_process[1]  # response time
            time += current_process[2]
            current_process[4] = time  # completion time
            current_process[7] = current_process[4] - current_process[1]  # waiting time
            current_process[6] = current_process[7] - current_process[2]  # turnaround time
            result_array.append(current_process)
            remaining_processes.remove(current_process)
        else:
            time += 1

    return result_array

def metrics(array):
    total_wait_time = 0
    for w in array:
        total_wait_time += w[6]

    total_turnaround_time = 0
    for t in array:
        total_turnaround_time += t[7]

    total_response_time = 0
    for r in array:
        total_response_time += r[5]

    average_wait_time = float(total_wait_time / len(array))
    average_turaround_time = float(total_turnaround_time / len(array))
    average_total_response_time = float(total_response_time / len(array))

    print("\n")
    print("Performance Metrics: ")
    print(f"Average Waiting Time: {average_wait_time:.2f}")
    print(f"Average Turnaround Time: {average_turaround_time:.2f}")
    print(f"Average Response Time: {average_total_response_time:.2f}")

    """ element [0] = name
        element [1] = arrival time
        element [2] = burst time
        element [3] = priority 
        element [4] = completion time 
        element [5] = response time
        element [6] = waiting time
        element [7] = turnaround time"""