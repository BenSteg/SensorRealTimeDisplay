# serialSensorRTDisplay
displays on one dynamic line sensor readout for integers &amp; binary. Using any serial bus transfer transfer data in the following form from device to computer running this code.  
  
TITLE_1,sensor_value_1,TITLE_2,sensor_value_2,...,TITLE_n,sensor_value_n,\n  
  
All titles must be 4 characters long (no more, no less). Once device is connected by serial bus code can be run in cmd. Output for this should look as shown below:  
```cmd
>py SensorSerial.py

connected to Serial: COM3

TFHS --- TFLS --- WFSw --- BPRP
0 ------ 0 ------ 0 ------ 0
```  
## Dependents

Argparse  
Serial  
Numpy  

## Arguments
Arguments are optional, the first argument '-c' is used for selecting the serial bus comms port being used. By default the program will connect to COM3 (can change this in the code if desired). However, any com port can be selected as shown below where COM2 is selected.  
  
```cmd
>py SensorSerial.py -c COM2

connected to Serial: COM2
```  
  
The second argument '-t' is for selecting the sensors you want to see. By default all sensor readouts will be displayed dynamically. by using '-t' you can select which sensors are displayed. Example of this is shown below.

```cmd
>py SensorSerial.py

connected to Serial: COM3

TFHS --- TFLS --- WFSw --- BPRP
0 ------ 0 ------ 0 ------ 0
```

And when '-t' is used.  

```cmd
>py SensorSerial.py -t TFHS WFSw TFLS

connected to Serial: COM3

TFHS --- TFLS --- WFSw
0 ------ 0 ------ 0
```
  
Sometimes the Order at which the sensors are readout is not first to last however titles will always match readout below.

## Example data transfer from arduino
this is an example from an arduino project I am doing starts with the title and has deliminator ',' and then the sensor value with no spaces anywhere. end with Serial.println(',') to provide the last deliminator and the '\n' which signifies the end of the bus message to our python program.   
```c++
// print data to serial bus
Serial.print("TFHS,");
Serial.print(TankFloatHighSwitch);
Serial.print(",TFLS,");
Serial.print(TankFloatLowSwitch);
Serial.print(",WFSw,");
Serial.print(WellFloatSwitch);
Serial.print(",BPRP,");
Serial.print(BorePumpRelayPinInd);
Serial.print(",IPRP,");
Serial.print(IrrigationPumpRelayPinInd);
Serial.print(",BVPC,");
Serial.print(BoreValvePinCloseInd);
Serial.print(",BVPO,");
Serial.print(BoreValvePinOpenInd);
Serial.print(",HaEP,");
Serial.print(HallEffectPin);
Serial.print(",LiMe,");
Serial.print(LightMeterPin);
Serial.print(",SECO,");
Serial.print(t.sec);
Serial.print(",BPIn,");
Serial.print(BorePumpInhibit);
Serial.println(",");
```
  
This will give the following readout on the cmd:  
```cmd
>py SensorSerial.py

connected to Serial: COM3

TFHS --- TFLS --- WFSw --- BPRP --- IPRP --- BVPC --- BVPO --- HaEP --- LiMe --- SECO --- BPIn
0 ------ 0 ------ 0 ------ 0 ------ 0 ------ 0 ------ 0 ------ 14 ------ 15 ------ 2 ------ 0
```
