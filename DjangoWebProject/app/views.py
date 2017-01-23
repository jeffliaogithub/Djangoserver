"""
Definition of views.
"""
import os
import sys
from django.conf import settings
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
from itertools import groupby
from django.urls import reverse
from django.urls import resolve
from plotutil import GetData
from plotutil import PreparePlotDataWithTime
from plotutil import  PlotData
from plotutil import  PreparePlotWithDate
from plotutil import convertdatetodaystring
from .forms import NameForm



def converttodate(string):  
    tmp = string.split()
    tmp = tmp[1].split(":")
    offset = -1*(len(tmp[3])+2)
    date = datetime.strptime(string[:offset], "%d/%m/%Y %H:%M:%S")
    return date

def key_function(x):        
    return (x[0].date())

datapath = "mydata" 

def preparedata():    
    data = []
    if os.path.isfile(datapath):
        with open(datapath) as f:
            for line in f:   
                line = line.rstrip()  
                try:               
                    date, cigarette = line.split(",")            
                    dateobject = converttodate (date)
                    data.append((dateobject,cigarette))  
                except:
                    pass
            

    data = sorted(data, key=key_function ,reverse = True)
    d=[]
    for k, g in groupby(data,key=key_function):   
        sum = 0.0
        newlist = []
        for x in g:
            sum+=float(x[1])    
            newlist.append((x[0].isoformat(),x[1]))    
        d.append([k.strftime('%d/%m/%Y'),str(sum),newlist])     
    return d

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""    
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def cigarette(request):
    """Renders the about page."""    
    if request.method == 'POST':
        readstring = request.body
        readstring = readstring.decode("ascii") 
        if not os.path.isfile(datapath):
            f = open(datapath,'w')
        else:
            f = open(datapath,'a')        
        f.write(readstring+"\n")
        f.close() # you can omit in most cases as the destructor will call it        
    data = preparedata()
    assert isinstance(request, HttpRequest)
    
    return render(
        request,
        'app/cigarette.html',
        {
            'title':str.format("{0} you have smoked {1} cigarette",data[0][0],data[0][1]),            
            'message':'Your application description page.',
            'year':datetime.now().year,
            'data_list':data
        }
    )




def facebook(request):
    
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        print(request.POST)
        form = NameForm(request.POST)                
        if form.is_valid():
            subject = form.cleaned_data['username']
            print(subject)
            subject = form.cleaned_data['password']
            print(subject)
        
        

    return render(
        request,
        'app/facebook.html',
        #'app/facebooklogin.html',
        {
            
        }
    )

def detail(request):
    """Renders the about page."""   
    tmpfilename = "app/static/temp/test.png"    
    try:
        data =  GetData (datapath,request.GET["date"])
        test = PreparePlotDataWithTime(data)
        PlotData(test,request.GET["date"],convertdatehourtoAMPM,tmpfilename)    
    except:
       data = GetData(datapath)
       test = PreparePlotWithDate(data)
       PlotData(test,"average",convertdatetodaystring,tmpfilename)    

    assert isinstance(request, HttpRequest)
    
    return render(
        request,
        'app/detail.html',
        {
            'title':"",            
            'picturename':tmpfilename[tmpfilename.find("/static"):],
            'year':datetime.now().year,            
        }
    )
