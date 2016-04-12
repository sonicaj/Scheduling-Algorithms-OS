def getKey(data,currentTime,curKey,completed):
    key = curKey
    if curKey == -1:
        minimum = 99999
        for d in data:
            if data[d]['name'] in completed:
                continue
            elif data[d]['rt'] < minimum and data[d]['at'] <= currentTime: 
                minimum = data[d]['rt']
                key = d
        key = None if key == -1 else key
    elif curKey == None:
        for d in data:
            if data[d]['at'] == currentTime:
                key = d
    else:
        for d in data:
            if data[d]['at'] > currentTime:
                continue
            elif data[d]['name'] in completed:
                continue
            elif curKey != None and data[d]['at'] <= currentTime and data[d]['rt'] < data[curKey]['rt'] and data[d]['rt'] < data[key]['rt'] :
                key = d
    return key

def getArrivalKey(data,currentTime,arrival):
    key = None
    for d in data:
        if data[d]['name'] in arrival:
            continue
        elif data[d]['at'] == systemTime:
            key = d
    return key
    
if __name__ == "__main__":
    file = open("input.txt", 'r')
    line = file.readline();data = dict();count = 1
    while line != '':
        arr = line.split(' ')
        data[count] = {'name': arr[0], 'at':int(arr[1]), 'bt':int(arr[2]),'rt':int(arr[2]),'response_time':-1,'waiting_time':-1,'turnaround_time':-1,'check':0}
        count += 1;line = file.readline()
    count = 0;name = dict();systemTime = 0;arrival = dict();check = False;
    key = getKey(data, systemTime, None,name)
    if key != None:
        arrival[data[key]['name']] = data[key]['name']
        print(data[key]['name'], ' has arrived in the ready queue at current system time being : ', systemTime)
        print('Details of this Process are ', data[key]);
        print(data[key]['name'],' is STARTING EXECUTION and the current system Time is',systemTime)
        data[key]['response_time'] = systemTime - data[key]['at']
        data[key]['check'] = 1
    while count < len(data):
        innerLoop = 1
        while innerLoop < 10000:
            systemTime = systemTime + 1 if innerLoop % 9999 == 0 else systemTime
            if innerLoop % 9999 == 0 and key != None:
                data[key]['rt']-=1
            arrivalKey = getArrivalKey(data, systemTime, arrival)
            if arrivalKey != None:
                arrival[data[arrivalKey]['name']] = data[arrivalKey]['name']
                print(data[arrivalKey]['name'], ' has arrived in the ready queue at current system time being : ', systemTime)
                print('Details of this Process are ', data[arrivalKey]);
            prevKey = key
            key = getKey(data, systemTime, key,name)
            if key != None and key != prevKey :
                if data[key]['check'] == 0:
                    data[key]['response_time'] = systemTime - data[key]['at']
                    data[key]['check'] = 1
                if prevKey != None:
                    print(data[prevKey]['name']," is moving to queue and ",data[key]['name'],' is STARTING EXECUTION and the current system Time is',systemTime )
                else:
                    print(data[key]['name'],' is STARTING EXECUTION and the current system Time is',systemTime)
            if key != None and data[key]['rt'] == 0:
                print("Process ",data[key]['name'],'has FINISHED EXECUTION at system Time ',systemTime)
                data[key]['waiting_time'] = systemTime - data[key]['at']-data[key]['bt']
                data[key]['turnaround_time'] = systemTime - data[key]['at']
                count += 1;check = True;name[data[key]['name']] = data[key]['name'];break;
            innerLoop = innerLoop + 1 if innerLoop != 9999 else 1
        if check == True:
            key = getKey(data, systemTime, -1,name);check = False
            if key != None:
                print(data[key]['name'],' is now STARTING EXECUTION')
                if data[key]['check'] == 0:
                    data[key]['response_time'] = systemTime - data[key]['at']
                    data[key]['check'] = 1
    avgTurnaround,avgResponse,avgWaiting = 0,0,0
    print("The waiting and turnaroud Times of each process is as follows : ")
    for d in data:
        print('Process ',data[d]['name'],' has Waiting Time : ',data[d]['waiting_time'])
        print('Process ',data[d]['name'],' has Turn around Time : ',data[d]['turnaround_time'])
        print('Process ',data[d]['name'],' has Response Time : ',data[d]['response_time'], '\n\n')
        avgTurnaround += data[d]['turnaround_time']
        avgResponse += data[d]['response_time']
        avgWaiting += data[d]['waiting_time']
    avgResponse /= len(data); avgTurnaround /= len(data); avgWaiting /= len(data);
    print("\n\nAverage Turnaround Time is : ",avgTurnaround,'\nAverage Waiting Time is : ',avgWaiting,'\nAverage Response Time is : ',avgResponse)