def getKey(data,currentTime,name):
    key = None;minimum = 99999
    for d in data:
        if data[d]['name'] in name:
            continue
        elif data[d]['at'] < minimum and data[d]['at'] <= currentTime:
            minimum = data[d]['at']
            key = d
    return key
if __name__ == "__main__":
    file = open("input.txt", 'r')
    line = file.readline();data = dict();count = 1
    while line != '':
        arr = line.split(' ')
        data[count] = {'name': arr[0], 'at':int(arr[1]), 'bt':int(arr[2]),'response_time':-1,'waiting_time:':-1,'turnaround_time':-1}
        count += 1;line = file.readline()
    count = 0;finishingTime = 0;name = dict();done = dict()
    key = getKey(data, finishingTime, done)
    if key != None:
        done[data[key]['name']] =data[key]['name'] 
        print(data[key]['name'], ' has arrived in the ready queue at current system time being : ', finishingTime)
    print('Details of this Process are ', data[1])
    while count < len(data):
        innerLoop = 0; 
        if key != None:
            print(data[key]['name'], ' IS STARTING EXECUTION')
            data[key]['response_time'] = finishingTime - data[key]['at']
        condition = data[key]['bt'] if key != None else 1
        while innerLoop < 1000 * condition:
            finishingTime = finishingTime + 1 if innerLoop % 1000 == 0 else finishingTime
            for d in data:
                if data[d]['name'] in name:
                    continue
                elif data[d]['at'] == finishingTime:
                    name[data[d]['name']] = data[d]['name']
                    print(data[d]['name'], ' has arrived in the ready queue at current system time being : ', finishingTime)
                    print('Details of this Process are ', data[d])
            innerLoop += 1
        if key != None:
            print(data[key]['name'], ' HAS FINISHED EXECUTION with a burst time of ', data[key]['bt'], ' and the finishing Time is : ', finishingTime)
            data[key]['turnaround_time'] = finishingTime - data[key]['at']
            data[key]['waiting_time'] = data[key]['turnaround_time'] - data[key]['bt']
            count += 1
        key = getKey(data, finishingTime, done)
        if key != None:
            done[data[key]['name']] =data[key]['name']
    avgTurnaround,avgResponse,avgWaiting = 0,0,0
    print("The waiting and turnaroud Times of each process is as follows : ")
    for d in data:
        print('Process ',data[d]['name'],' has Waiting Time : ',data[d]['waiting_time'])
        print('Process ',data[d]['name'],' has Turn around Time : ',data[d]['turnaround_time'])
        print('Process ',data[d]['name'],' has Response Time : ',data[d]['response_time'],'\n\n')
        avgTurnaround += data[d]['turnaround_time']
        avgResponse += data[d]['response_time']
        avgWaiting += data[d]['waiting_time']
    avgResponse /= len(data); avgTurnaround /= len(data); avgWaiting /= len(data);
    print("\n\nAverage Turnaround Time is : ",avgTurnaround,'\nAverage Waiting Time is : ',avgWaiting,'\nAverage Response Time is : ',avgResponse)
        