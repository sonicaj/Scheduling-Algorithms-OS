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
    def getSize(self):
        return len(self.queue)
    
class CompletedQueue:
    def __init__(self):
        self.queue = []
    def enqueue(self,process):
        self.queue.append(process)

class AuxiliaryQueue:
    def __init__(self):
        self.queue =[]
    def checkEmpty(self):
        return True if not self.queue else False
    def enqueue(self,process):
        self.queue.append(process)
    def dequeue(self):
        return self.queue.pop(0)

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
    if len(check) == 0:
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

def exchangeQueues(queue1,queue2):
    while queue1.checkEmpty() == False:
        queue2.enqueue(queue1.dequeue())
        
def MLT(queues,arriving):
    global systemTime
    readyQueue1 = ReadyQueue()
    readyQueue2 = ReadyQueue()
    completedQueue = CompletedQueue()
    queueNo = 0;check = True
    waitingQueue = WaitingQueue()
    while readyQueue1.checkEmpty() == False or readyQueue2.checkEmpty() == False or isEmpty(arriving) == False:
        if queues[queueNo]['name'] == "RR":
            print("Executing RR Queue")
            cpu = CPU(queues[queueNo]['ts'])
            while readyQueue2.checkEmpty == True or check == True or readyQueue1.checkEmpty() != True or cpu.checkIdle() != True or waitingQueue.checkEmpty() != True:
                while isArriving(arriving) != False:
                    readyQueue1.enqueue(checkArrival(arriving))
                while waitingQueue.checkReturn() == True:
                    readyQueue1.enqueue(waitingQueue.dequeue())
                if cpu.checkIdle() == False:
                    string,process = cpu.runningState()
                    if string != "running":
                        if string == "ready":
                            print(process.name, " is going to " ,queues[queueNo + 1]['name']," Queue from CPU at system Time ",systemTime)
                            readyQueue2.enqueue(process)
                        elif string == "completed":
                            completedQueue.enqueue(process)
                            print(process.name, " has completed it's task at system TIme ",systemTime)
                        elif string == "waiting":
                            waitingQueue.enqueue(process)
                            print(process.name, " is going to waiting queue at system TIme ",systemTime)
                if cpu.checkIdle() == True:
                    if readyQueue1.checkEmpty() == False:
                        check = False
                        entercputemp = readyQueue1.dequeue()
                        cpu.enterCPU(entercputemp)
                #print(entercputemp.name," is entering CPU at system Time ",systemTime)
                systemTime += 1
                #time.sleep(1)
        elif queues[queueNo]['name'] == "VRR":
            print("Executing VRR Queue")
            auxiliaryQueue = AuxiliaryQueue()
            cpu = CPU(queues[queueNo]['ts'])
            while readyQueue2.checkEmpty == True or check == True or readyQueue1.checkEmpty() != True or waitingQueue.checkEmpty() != True or cpu.checkIdle() != True:
                while isArriving(arriving) != False:
                    readyQueue1.enqueue(checkArrival(arriving))
                while waitingQueue.checkReturn() == True:
                    waitingDequeue = waitingQueue.dequeue()
                    if waitingDequeue.timeSlice == timeSlice:
                        readyQueue1.enqueue(waitingDequeue)
                    else:
                        auxiliaryQueue.enqueue(waitingDequeue)
                if cpu.checkIdle() == False:
                    string,process = cpu.runningState()
                    if string != "running":
                        if string == "waiting":
                            print(process.name," is going to Waiting Queue at system Time ",systemTime)
                            waitingQueue.enqueue(process)
                        elif string == "ready":
                            print(process.name, " is going to " ,queues[queueNo + 1]['name']," Queue from CPU at system Time ",systemTime)
                            readyQueue2.enqueue(process)
                        elif string == "completed":
                            completedQueue.enqueue(process)
                            print(process.name, " has completed it's task at system TIme ",systemTime)
                if cpu.checkIdle() == True:
                    if auxiliaryQueue.checkEmpty() == False:
                        check = False
                        entercputemp = auxiliaryQueue.dequeue()
                        cpu.enterCPU(entercputemp)
                    elif readyQueue1.checkEmpty() == False:
                        check = False
                        entercputemp = readyQueue1.dequeue()
                        cpu.enterCPU(entercputemp)
                #print(entercputemp.name," is entering CPU at system Time ",systemTime)
                systemTime += 1
                #time.sleep(1)
        elif queues[queueNo]['name'] == "FCFS":
            print("Executing FCFS Queue")
            while check == True or readyQueue1.checkEmpty() != True or isEmpty(arriving) != True:
                check = False
                process = readyQueue1.dequeue()
                print(process.name, " is going into execution at system time ",systemTime)
                endTime = systemTime + process.remainingTime
                i = systemTime
                while i < endTime:
                    if process.cpuRemainingTime == 0:
                        endTime += process.IOTime
                        process.waitingFinishTime = systemTime + process.IOTime
                    if process.waitingFinishTime == systemTime:
                        process.cpuRemainingTime = process.cpuTime
                    systemTime += 1
                    i += 1
                print(process.name, " has finished execution at system time ",systemTime)
                completedQueue.enqueue(process)
        exchangeQueues(readyQueue2, readyQueue1)
        queueNo += 1
    
if __name__ == "__main__":
    file = open("MLT.txt", 'r')
    queue = dict()
    data = dict()
    count = 1
    countQueue = file.readline();
    countQueue = int(countQueue)
    i = 0
    while i < countQueue:
        line = file.readline()
        arr = line.split(' ')
        if arr[0] == "FCFS\n":
            queue[i] = {'name':arr[0][:4],'ts':None}
        else:
            queue[i] = {'name':arr[0],'ts':int(arr[1])}
        i += 1
    line = file.readline()
    while line != '':
        arr = line.split(' ')
        if arr[0] == "C":
            data[count] = {'name': arr[1], 'at':int(arr[2]), 'bt':int(arr[3]),'cpu':int(arr[3]) + 1,'io':0}
        else:
            data[count] = {'name': arr[1], 'at':int(arr[2]), 'bt':int(arr[3]),'cpu':int(arr[4]),'io':int(arr[5])}
        count += 1;line = file.readline()
    MLT(queue, data)
    
