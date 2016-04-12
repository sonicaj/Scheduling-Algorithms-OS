def getKey(data,currentTime,name):
    minimum = 99999;key = None
    for d in data:
        if data[d]['name'] in name:
            continue
        elif data[d]['at'] <= currentTime and data[d]['bt'] <= minimum:
            minimum = data[d]['bt']
            key = d
    return key

def getArrivalKey(data,currentTime,name):
    key = None
    for d in data:
        if data[d]['name'] in name:
            continue
        elif data[d]['at'] == currentTime:
            key = d
    return key
    
if __name__ == "__main__":
    file = open("input.txt", 'r')
    line = file.readline();data = dict();count = 1
    while line != '':
        arr = line.split(' ')
        data[count] = {'name': arr[0], 'at':int(arr[1]), 'bt':int(arr[2]),'response_time':-1,'waiting_time:':-1,'turnaround_time':-1}
        count += 1;line = file.readline()
    count = 0;name = dict();finishingTime = 0;check = False;arrival = dict();prev = 0
    key = getKey(data,finishingTime,name)
    if key != None:
        arrival[data[key]['name']] = data[key]['name']
        print(data[key]['name'], ' has arrived in the ready queue at current system time being : ', finishingTime)
        print('Details of this Process are ', data[key]);check = True;
    while count < len(data):
        innerLoop = 1
        if check == True:
            if not name :
                prev = finishingTime
            name[data[key]['name']] = data[key]['name']
            print(data[key]['name'], ' IS STARTING EXECUTION')
            data[key]['response_time'] = finishingTime - data[key]['at']
        while innerLoop < 10000:
            finishingTime = finishingTime + 1 if innerLoop % 9999 == 0 else finishingTime
            at = getArrivalKey(data, finishingTime, arrival)
            if at != None:
                arrival[data[at]['name']] = data[at]['name']
                print(data[at]['name'], ' has arrived in the ready queue at current system time being : ', finishingTime)
                print('Details of this Process are ', data[at]);
            if check == True and finishingTime == prev + data[key]['bt']:
                print(data[key]['name'], ' HAS FINISHED EXECUTION with a burst time of ', data[key]['bt'], ' and the finishing Time is : ', finishingTime)
                data[key]['turnaround_time'] = finishingTime - data[key]['at']
                data[key]['waiting_time'] = data[key]['turnaround_time'] - data[key]['bt']
                check = False;prev = finishingTime;count +=1;break
            elif check == False:
                key = getKey(data, finishingTime, name)
                if key != None:
                    check = True
                    break;
            innerLoop = innerLoop + 1 if innerLoop != 9999 else 1
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