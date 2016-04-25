import time
global systemTime
systemTime = 0
class Process:
    def __init__(self,name,arrivalTime,burstTime,cpuTime,IOTime):
        self.name = name
        self.arrivalTime = arrivalTime
        self.finishTime = None
        self.burstTime = burstTime
        self.cpuTime = cpuTime # time after which it will take input output
        self.IOTime = IOTime
        self.responseTime = 0
        self.turnAroundTime = 0
        self.remainingTime = burstTime
        self.waitingFinishTime = None
        self.cpuRemainingTime = cpuTime # remiain time in cpu after which it will go for input output
        self.timeSlice = None

class ReadyQueue:
    def __init__(self):
        self.queue = []
    def checkEmpty(self):
        return True if not self.queue else False
    def enqueue(self,process):
        self.queue.append(process)
    def dequeue(self):
        return self.queue.pop(0)
class CompletedQueue:
    def __init__(self):
        self.queue = []
    def enqueue(self,process):
        self.queue.append(process)

class WaitingQueue:
    def __init__(self):
        self.queue = []
    def checkEmpty(self):
        return True if not self.queue else False
    def enqueue(self,process):
        self.queue.append(process)
    def checkReturn(self):
        i = 0
        for d in self.queue:
            if self.queue[i].waitingFinishTime == systemTime:
                return True
        i += 1
        return False
    def dequeue(self):
        self.queue[0].cpuRemainingTime = self.queue[0].cpuTime if self.queue[0].waitingFinishTime == systemTime else self.queue[0].cpuRemainingTime
        return self.queue.pop(0) if self.queue[0].waitingFinishTime == systemTime else None

class CPU:
    def __init__(self,timeSlice):
        self.name = "CPU"
        self.process = None
        self.timeSlice = timeSlice
    def enterCPU(self,process):
        self.process = process if self.process == None else self.process
        self.process.timeSlice = self.timeSlice if self.process.timeSlice == None else self.process.timeSlice
        return True if self.process == process else False
    def checkIdle(self):
        return True if self.process == None else False
    def runningState(self):
        temp = self.process
        if self.process.remainingTime == 0:
            self.process = None
            return ['completed',temp]
        if self.process.cpuRemainingTime == 0:
            self.process = None
            temp.waitingFinishTime = systemTime + temp.IOTime
            return ['waiting',temp]
        if self.process.timeSlice == 0:
            self.process = None
            temp.timeSlice = self.timeSlice
            return ['ready',temp]
        self.process.remainingTime -= 1
        self.process.timeSlice -= 1
        self.process.cpuRemainingTime -= 1
        if self.process.remainingTime == 0:
            self.process = None
            return ['completed',temp]
        if self.process.cpuRemainingTime == 0:
            self.process = None
            temp.waitingFinishTime = systemTime + temp.IOTime
            return ['waiting',temp]
        if self.process.timeSlice == 0:
            self.process = None
            temp.timeSlice = self.timeSlice
            return ['ready',temp]
        return ["running",None]
    def checkExit(self):
        if self.process.cpuRemainingTime == 0 or self.process.timeSlice == 0 or self.process.remainingTime == 0:
            return True
        else:
            return False
def isArriving(processes):
    for d in processes:
        if processes[d]['at'] == systemTime:
            return True
    return False

def isEmpty(check):
    if not check:
        return True
    else:
        return False

def checkArrival(processes):
    for d in processes:
        if processes[d]['at'] == systemTime:
            process = Process(processes[d]['name'],processes[d]['at'],processes[d]['bt'],processes[d]['cpu'],processes[d]['io'])
            del processes[d]
            return process
    return None

def RoundRobin(timeSlice,arriving):
    global systemTime
    readyQueue = ReadyQueue()
    waitingQueue = WaitingQueue()
    completedQueue = CompletedQueue()
    cpu = CPU(timeSlice)
    while isEmpty(arriving) != True or readyQueue.checkEmpty() != True or waitingQueue.checkEmpty() != True or cpu.checkIdle() != True:
        while isArriving(arriving) != False:
            readyQueue.enqueue(checkArrival(arriving))
        while waitingQueue.checkReturn() == True:
            readyQueue.enqueue(waitingQueue.dequeue())
        if cpu.checkIdle() == False:
            string,process = cpu.runningState()
            if string != "running":
                if string == "waiting":
                    print(process.name," is going to Waiting Queue at system Time ",systemTime)
                    waitingQueue.enqueue(process)
                elif string == "ready":
                    print(process.name, " is going to Ready Queue from CPU at system Time ",systemTime)
                    readyQueue.enqueue(process)
                elif string == "completed":
                    completedQueue.enqueue(process)
                    print(process.name, " has completed it's task at system TIme ",systemTime)
        if cpu.checkIdle() == True:
            if readyQueue.checkEmpty() == False:
                entercputemp = readyQueue.dequeue()
                cpu.enterCPU(entercputemp)
                #print(entercputemp.name," is entering CPU at system Time ",systemTime)
        systemTime += 1
        time.sleep(1)
        
if __name__ == "__main__":
    file = open("inputRR.txt", 'r')
    line = file.readline()
    timeSlice = int(line)
    line = file.readline();data = dict();count = 1
    while line != '':
        arr = line.split(' ')
        if arr[0] == "C":
            data[count] = {'name': arr[1], 'at':int(arr[2]), 'bt':int(arr[3]),'cpu':int(arr[3]) + 1,'io':0}
        else:
            data[count] = {'name': arr[1], 'at':int(arr[2]), 'bt':int(arr[3]),'cpu':int(arr[4]),'io':int(arr[5])}
        count += 1;line = file.readline()
    RoundRobin(timeSlice, data)