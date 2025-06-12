# Bank Algorithm Implementation

class Process:
    def __init__(self,name:str,resource_num:int,max_resource:list[int],
                 allocation:list[int]) -> None:
        if len(max_resource) != resource_num:
            raise ValueError("Max resources length must match resource number")  
        if len(allocation) != resource_num:
            raise ValueError("Allocation length must match resource number")
        self.name = name
        self.resource_num = resource_num
        self.max_resource = max_resource
        self.allocation = allocation
        self.need = [max_resource[i] - allocation[i] for i in range(resource_num)]
        self.is_finished = False
        self.next_process:Process | None = None
        self.prev_process:Process | None = None

    def __repr__(self) -> str:
        return f"Process({self.name}, max_resource={self.max_resource}, allocation={self.allocation}, need={self.need})"

    def __str__(self) -> str:
        return f"Process {self.name}: Max={self.max_resource}, Allocated={self.allocation}, Need={self.need}, Finished={self.is_finished}"

    def check_finished(self) -> bool:
        if all(self.need[i] == 0 for i in range(self.resource_num)):
            self.is_finished = True
            if self.prev_process:
                self.prev_process.next_process = self.next_process
            if self.next_process:
                self.next_process.prev_process = self.prev_process
            return True
        return False

class ProcessList:
    def __init__(self) -> None:
        self.head:Process | None = None
        self.tail:Process | None = None

    def add_process(self,process:Process) -> None:
        if not self.head:
            self.head = process
            self.tail = process
        elif self.tail is not None:
            self.tail.next_process = process
            process.prev_process = self.tail
            self.tail = process

    def remove_process(self,process:Process) -> None:
        if not self.head:
            raise ValueError("Process list is empty")
        if process == self.head:
            self.head = process.next_process
            if self.head:
                self.head.prev_process = None
        elif process == self.tail:
            self.tail = process.prev_process
            if self.tail:
                self.tail.next_process = None
        else:
            if process.prev_process:
                process.prev_process.next_process = process.next_process
            if process.next_process:
                process.next_process.prev_process = process.prev_process
        process.next_process = None
        process.prev_process = None

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next_process

class BankAlgorithm:
    def __init__(self,resource_num:int,total_resources:list[int]) -> None:
        super().__init__()
        if resource_num <= 0:
            raise ValueError("Resource number must be greater than zero")
        if len(total_resources) != resource_num:
            raise ValueError("Total resources length must match resource number")
        if any(r < 0 for r in total_resources):
            raise ValueError("Total resources cannot be negative")
        self.resource_num = resource_num
        self.total_resources = total_resources
        self.processes_list:ProcessList = ProcessList()
        self.available_resources = total_resources
        
    def add_process(self,process:Process) -> None:
        self.processes_list.add_process(process)
        self.available_resources = [self.available_resources[i] - process.allocation[i] for i in range(self.resource_num)]
        if any(r < 0 for r in self.available_resources):
            raise ValueError("Total resources cannot be less than allocated resources")
        
    def request_resources(self,process_name:str,request:list[int]) -> bool:
        """Request resources for a process and check if the system remains in a safe state."""
        if len(request) != self.resource_num:
            raise ValueError("Request length must match resource number")
        process = next((p for p in self.processes_list if p.name == process_name), None)
        if not process:
            raise ValueError(f"Process {process_name} not found")
        if any(request[i] > process.need[i] for i in range(self.resource_num)):
            raise ValueError("Request exceeds process's need")
        if any(request[i] > self.available_resources[i] for i in range(self.resource_num)):
            raise ValueError("Request exceeds available resources")
        # Temporarily allocate resources
        for i in range(self.resource_num):
            self.available_resources[i] -= request[i]
            process.allocation[i] += request[i]
            process.need[i] -= request[i]
        # Check for safe state
        is_safe,safe_sequence = self.check_safe_state()
        if not is_safe:
            # Rollback allocation
            for i in range(self.resource_num):
                self.available_resources[i] += request[i]
                process.allocation[i] -= request[i]
                process.need[i] += request[i]
            return False
        print(f"Resources allocated to {process_name}. A possible safe sequence:")
        assert safe_sequence is not None, "Safe sequence should not be None"
        print('\n'.join([f'{str(p[1])}, Work={p[0]}' for p in safe_sequence]))
        return True
    
    def release_resources(self,process_name:str,release:list[int]) -> None:
        """Release resources allocated to a process temporarily."""
        process = next((p for p in self.processes_list if p.name == process_name), None)
        if not process:
            raise ValueError(f"Process {process_name} not found")
        if any(release[i] > process.allocation[i] for i in range(self.resource_num)):
            raise ValueError("Release exceeds allocated resources")
        # Release resources
        for i in range(self.resource_num):
            self.available_resources[i] += release[i]
            process.allocation[i] -= release[i]
            process.need[i] += release[i]
        
    def check_safe_state(self) -> tuple[bool, list[tuple[list[int],Process]] | None]:
        """Check if the system is in a safe state.
        :return: 系统是否安全以及申请资源时的安全性检查表格
        """
        work = self.available_resources[:]
        works:list[list[int]] = list()
        finish = {p.name: False for p in self.processes_list}
        safe_sequence:list[Process] = list()
        while True:
            found = False
            for process in self.processes_list:
                if not finish[process.name] and all(process.need[i] <= work[i] for i in range(self.resource_num)):
                    # Simulate allocation
                    works.append(work[:])
                    for i in range(self.resource_num):
                        work[i] += process.allocation[i]
                    finish[process.name] = True
                    safe_sequence.append(process)
                    found = True
            if not found:
                break
        if all(finish.values()):
            return True, list(zip(works, safe_sequence))
        return False, None
    
    def __repr__(self) -> str:
        return f"BankAlgorithm(resource_num={self.resource_num}, total_resources={self.total_resources}, available_resources={self.available_resources})"
    
    def display_processes(self) -> None:
        """Display all processes in the system."""
        if not self.processes_list.head:
            print("No processes in the system.")
            return
        print("Processes in the system:")

        for process in self.processes_list:
            print(process)

def main() -> None:
    # Example usage
    bank = BankAlgorithm(3, [9, 3, 6])
    
    p1 = Process("P1", 3, [3, 2, 2], [1, 0, 0])
    p2 = Process("P2", 3, [6, 1, 3], [5, 1, 1])
    p3 = Process("P3", 3, [3, 1, 4], [2, 1, 1])
    p4 = Process("P4", 3, [4, 2, 2], [0, 0, 2])
    
    bank.add_process(p1)
    bank.add_process(p2)
    bank.add_process(p3)
    bank.add_process(p4)
    
    bank.display_processes()
    
    # Request resources for P2
    if bank.request_resources("P2", [1, 0, 1]):
        print("Request for P2 granted.")
    else:
        print("Request for P2 denied.")
    
    # Request resources for P1
    if bank.request_resources("P1", [0, 0, 1]):
        print("Request for P1 granted.")
    else:
        print("Request for P1 denied.")

    # Request resources for P3
    if bank.request_resources("P3", [0, 0, 1]):
        print("Request for P3 granted.")
    else:
        print("Request for P3 denied.")

    # Release resources for P2
    # bank.release_resources("P2", [1, 0, 0])
    
    # Check safe state
    is_safe, safe_sequence = bank.check_safe_state()
    if is_safe:
        assert safe_sequence is not None, "Safe sequence should not be None"
        print("System is in a safe state.")
        print(f"Safe sequence:\n{'\n'.join(str(p[1]) for p in list(safe_sequence))}", )
    else:
        print("System is not in a safe state.")

if __name__ == "__main__":
    main()