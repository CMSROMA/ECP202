import npyscreen
from ECP202Wrapper import ECP202
import csv
import time

ecp202 = ECP202('/dev/ttyUSB1')
print('Status %d'%ecp202.getDeviceStatus())
print('Alarm Status %d'%ecp202.getAlarmStatus())
print('IO Status %d'%ecp202.getIOStatus())
print('Fan settings %d'%ecp202.getFanSettings())
print('Temperature %3.1f'%ecp202.getAmbientTemperature())
print('Evaporator temperature %3.1f'%ecp202.getEvaporatorTemperature())
print('Target Temperature %3.1f'%ecp202.getTargetTemperature())
print('DeltaT Taget Temperature %3.1f'%ecp202.getDeltaTemperature())
#print('Set Fan settings to 0'%ecp202.setFanSettings(0))
#time.sleep(1)
#print('Fan settings %d'%ecp202.getFanSettings())
