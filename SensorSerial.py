import argparse
import serial
import numpy as np

#Space Holders for global data
serialString = b''
readOut = ""
titleLengths = []
sensorValuesFiltered = []
titleFiltered = []

#SETUP argparse
parser = argparse.ArgumentParser(description='Setup Sensor display.')
parser.add_argument('-c', '--comms', type=str, help="Select the comms port to be used e.g. COM3")
parser.add_argument('-b', '--baudrate', type=int, help="Select the baudrate for serial comms, default 9600")
parser.add_argument('-t', '--title', nargs='*', help='sensor titles 4 letters only can be sourced from serial bus')
args = parser.parse_args()

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

def splitSerialData(serialIn):
    #Convert Serial binary to string
    readOut = serialIn.decode()
    #Seperate using deliminator
    serialStringTable = readOut.split(',', -1)
    sensorTitle = serialStringTable[::2]
    sensorValue = serialStringTable[1::2]
    return(sensorTitle, sensorValue)
    
def show_output_single_line(out):
    print("\r", end='')
    print(f"{' ------ '.join([item for item in out[:]])}", end='', flush=True)

def TableTitle(Titles):
    #Prints Titles
    print(f"{' --- '.join([item for item in Titles[:]])}")

def convert_List_To_String(lst, seperator=''):
    #Convert list to string
    return seperator.join(lst)

if __name__ == '__main__':
    #Connect to Comms port of choice or default to COM3
    if args.comms:
        if args.baudrate:
            serialPort = SerialConnect(args.comms, args.baudrate)
        else:
            serialPort = SerialConnect(args.comms)
    else:
        if args.baudrate:
            serialPort = SerialConnect("COM3", args.baudrate)
        else:
            serialPort = SerialConnect("COM3")
    #Use given sensor titles or use default AAAA BBBB CCCC
    if args.title:
        titles = args.title
        #Check sensor title lengths are 4 and raise error if they are not.
        for i in titles:
            titleLengths.append(len(titles[titles.index(i)]))
            if len(titles[titles.index(i)]) != 4:
                print("\n!!!ERROR: Sensor titles must only be 4 values long\n")
                raise
    #Count's used for one time loops below to print of sensor titles
    count1, count2 = 0, 0
    #Start Main Loop
    while True:
        #Check serial buffer has been filled
        
        if(serialPort.in_waiting > 0):
            #Read serial buffer into variable
            serialString = serialPort.readline()
            #Convert Serial data in into serial array of title and sensor values
            ardtitles, sensorValue = splitSerialData(serialString)
            #Print sensor titles
            
            if args.title:
                intersect, ind_ardtitles, ind_argtitles = np.intersect1d(ardtitles, args.title, return_indices=True)
                
                if count1 == 0:
                    
                    for i in ind_ardtitles:
                        titleFiltered.append(ardtitles[i])
                    titleStrArray = np.array(titleFiltered)
                    TableTitle(titleStrArray)
                    count1 += 1
                    titleFiltered.clear()
                
                for i in ind_ardtitles:
                    sensorValuesFiltered.append(sensorValue[i])
                
                sensorStrArray = np.array(sensorValuesFiltered)
                show_output_single_line(sensorStrArray)
                sensorValuesFiltered.clear()
                #show_output_single_line(sensorValue[:len(titles)])
            
            else:
                if count2 == 0:
                    del ardtitles[-1]
                    TableTitle(ardtitles)
                    
                    for i in ardtitles:
                        titleLengths.append(len(ardtitles[ardtitles.index(i)]))
                        if len(ardtitles[ardtitles.index(i)]) != 4:
                            print("\n!!!ERROR: Sensor titles must only be 4 values long\n")
                            raise
                    count2+=1
                #Print out dynamicly on a single line the sensor values
                show_output_single_line(sensorValue[:len(ardtitles)])
