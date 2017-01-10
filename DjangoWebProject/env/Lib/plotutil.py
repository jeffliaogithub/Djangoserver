import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
import time
from itertools import groupby
import dateutil.parser

def printsoftmax():
    scores = [3.0, 1.0, 0.2]
    def softmax(x):
        """Compute softmax values for each sets of scores in x."""
        return np.exp(x)/np.sum(np.exp(x),axis=0)
        #return x/np.sum(x,axis=0)


    print(softmax(scores))

    # Plot softmax curves
    import matplotlib.pyplot as plt
    x = np.arange(-2.0, 6.0, 1)
    print(x)
    scores = np.vstack([x, np.ones_like(x), 0.2 * np.ones_like(x)])
    print(scores)
    print(softmax(scores))
    print(x.shape)
    print(softmax(scores).shape)

    plt.plot(x, softmax(scores).T, linewidth=2)
    plt.show()

    functions = []
    functions.append(np.cos)

def converttodate(string):  
    tmp = string.split()
    tmp = tmp[1].split(":")
    offset = -1*(len(tmp[3])+2)
    date=datetime.datetime.strptime(string[:offset], "%d/%m/%Y %H:%M:%S")    
    return date

def key_function(x):        
    return (x[0].date())

def GetData(datafile,datestring = None):    
    data = []
    if os.path.isfile(datafile):
        with open(datafile) as f:
            for line in f:   
                line = line.rstrip()                 
                date, cigarette = line.split(",")
            
                dateobject = converttodate (date)
                data.append((dateobject,cigarette))  
            

    data = sorted(data, key=key_function)
    d=[]
    for k, g in groupby(data,key=key_function):   
        sum = 0.0
        newlist = []
        for x in g:            
                sum+=float(x[1])    
                newlist.append((x[0].isoformat(),x[1]))                
        if datestring == None:
            d.append([k.strftime('%d/%m/%Y'),str(sum),newlist])     
        elif    k.strftime('%d/%m/%Y') == datestring:
            d.append([k.strftime('%d/%m/%Y'),str(sum),newlist]) 

    return d

def convertdatetohour(date, time):   
    date = dateutil.parser.parse(date)   
    time = dateutil.parser.parse(time)    
    h = time-date
    return (time-date).seconds/3600

def convertdatetodays(date):   
    date = dateutil.parser.parse(date)   
    days = date - datetime.datetime(2017,1,1)    
    return days.days

def convertdatetodaystring(date):       
    date = datetime.datetime(2017,1,1) + datetime.timedelta(date)    
    return   date.strftime("'%m/%d/%Y'");

def convertdatehourtoAMPM(hour):       
    if hour == 12:
        return "12 PM";
    if hour == 0:
        return "12 AM";
    if (hour) // 12 :
        return str(hour % 12)+"PM"
    else:
        return str(hour % 12)+"AM"        

def PreparePlotDataWithTime(data):
    if len(data) == 1:
        data = data[0]
        targetdate = data[0]
        data = data[2]
        timepoint = []
        numberpoint = []
        for  x in data:
            timepoint.append(convertdatetohour(targetdate,x[0]))
            numberpoint.append(float(x[1]))        
        return  [timepoint,numberpoint]
    else:
        pass
def PreparePlotWithDate(data): 
    timepoint = []
    numberpoint = []
    for  x in data:
        timepoint.append(convertdatetodays(x[0]))
        numberpoint.append(float(x[1]))        
    return  [timepoint,numberpoint]    


def PlotData(data, title, conversion,savefile = None):

    plt.clf()
    plt.rc('xtick', labelsize=10) 
    plt.bar(data[0],data[1], color="red" , width = 0.1)  
    minimun = int(min(data[0]))-1
    maximum = int(max(data[0]))+1
    hours = [x for x in range(minimun,maximum)]
    lables = [conversion(x) for x in hours]   
    plt.xticks(hours,lables)
    
    plt.title(title)
    if savefile:
        plt.savefig(savefile)
    else:
        plt.show()

'''data = GetData("01/02/2017")
test = PreparePlotDataWithTime(data)
PlotData(test,"01/02/2017",convertdatehourtoAMPM,"test1.jpg")
#PlotData(test,"01/02/2017",convertdatehourtoAMPM)

data = GetData()
test = PreparePlotWithDate(data)
PlotData(test,"average",convertdatetodaystring,"test2.jpg")
#PlotData(test,"average",convertdatetodaystring)
'''