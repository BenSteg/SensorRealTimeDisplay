import serial
import numpy as np

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

def SerialConnect(COM, baudrate = 9600, bytesize = 8, timeout = 2, stopbits = serial.STOPBITS_ONE):
    #SETUP SERIAL
    try:
        serialPort = serial.Serial(port = COM,
                                  baudrate = baudrate,
                                  bytesize = bytesize,
                                  timeout = timeout,
                                  stopbits = stopbits)
        
        print("\nconnected to Serial: " + serialPort.portstr + "\n")
        #Flush the serial buffer so only reading real time data
        serialPort.flushInput()
        return(serialPort)
    except:
        print("\nFailed to connect to " + COM + "\n")
        raise

def setupSerial(COM=None, baudrate=None):
    if COM:
        if baudrate:
            serialPort = SerialConnect(COM, baudrate)
        else:
            serialPort = SerialConnect(COM)
    else:
        if baudrate:
            serialPort = SerialConnect("COM3", baudrate)
        else:
            serialPort = SerialConnect("COM3")
    return(serialPort)

def checkTitleLengths(title=None):
    titleLengths = []
    if title:
        titles = title
        #Check sensor title lengths are 4 and raise error if they are not. 
        #This is needed for spacing and also may cause errors later on with 
        #printing sensor values.
        for i in titles:
            titleLengths.append(len(titles[titles.index(i)]))
            if len(titles[titles.index(i)]) != 4:
                print("\n!!!ERROR: Sensor titles must only be 4 values long\n")
                raise

def splitSerialData(serialIn):
    #Convert Serial binary to string
    readOut = ""
    readOut = serialIn.decode()
    #Seperate using deliminator
    serialStringTable = readOut.split(',', -1)
    sensorTitle = serialStringTable[::2]
    sensorValue = serialStringTable[1::2]
    return(sensorTitle, sensorValue)

@run_once
def printArgumentTitles(ind_ardtitles, ardtitles):
    titleFiltered = []
    for i in ind_ardtitles:
        titleFiltered.append(ardtitles[i])
    #Need to convert list to numpy array otherwise dynamic 
    #printing wont work.
    titleStrArray = np.array(titleFiltered)
    TableTitle(titleStrArray)
    #need to clear the list for next serial bus read
    titleFiltered.clear()

@run_once
def printSerialTitles(ardtitles):
    titleLengths = []
    del ardtitles[-1]
    TableTitle(ardtitles)
    for i in ardtitles:
        titleLengths.append(len(ardtitles[ardtitles.index(i)]))
        if len(ardtitles[ardtitles.index(i)]) != 4:
            print("\n!!!ERROR: Sensor titles must only be 4 values long\n")
            raise
    return(ardtitles)
    
def showOutputSingleLine(out):
    print("\r", end='')
    print(f"{' ------ '.join([item for item in out[:]])}", end='', flush=True)

def TableTitle(Titles):
    #Prints Titles
    print(f"{' --- '.join([item for item in Titles[:]])}")