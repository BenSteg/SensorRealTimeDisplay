import argparse
import serial
import numpy as np
from SensorSerialFunctions import *

#Space Holders for serial data
serialString = b''
sensorValuesFiltered = []

#Setup arguments for comms, baudrate, and titles for sensors. all need to be 
#optional
parser = argparse.ArgumentParser(description='Setup Sensor display.')
parser.add_argument('-c',
                    '--comms', 
                    type=str, 
                    help="Select the comms port to be used, default COM3")
parser.add_argument('-b', 
                    '--baudrate', 
                    type=int, 
                    help="Select the baudrate for serial comms, default 9600")
parser.add_argument('-t', 
                    '--title', 
                    nargs='*', 
                    help='sensor titles 4 letters only can be sourced from \
                    serial bus')
args = parser.parse_args()

if __name__ == '__main__':
    #Connect ot serial port, either using default values or argument values
    serialPort = setupSerial(args.comms, args.baudrate)
    #show only the sensor specified in the arguments or show all sensor values 
    #from serial
    checkTitleLengths(args.title)

    while True:
        #Check serial buffer has been filled before proceeding with function
        if(serialPort.in_waiting > 0):
            serialString = serialPort.readline()
            ardtitles, sensorValue = splitSerialData(serialString)
            if args.title:
                _, ind_ardtitles, _ = np.intersect1d(ardtitles, 
                                                    args.title, 
                                                    return_indices=True)
                printArgumentTitles(ind_ardtitles, ardtitles)               
                for i in ind_ardtitles:
                    sensorValuesFiltered.append(sensorValue[i])
                #Need to convert list to numpy array otherwise dynamic 
                #printing wont work.
                sensorStrArray = np.array(sensorValuesFiltered)
                showOutputSingleLine(sensorStrArray)
                sensorValuesFiltered.clear()
            
            else:
                printSerialTitles(ardtitles)
                #have to remove last item in ardtitles as it is \n
                showOutputSingleLine(sensorValue[:len(ardtitles[:-1])])
