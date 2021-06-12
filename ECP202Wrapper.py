import minimalmodbus
from time import sleep


class ECP202:
    def __init__(self,port):
        self.port=port
        self.instrument = minimalmodbus.Instrument(self.port,1,mode=minimalmodbus.MODE_RTU)

        #Make the settings explicit
        self.instrument.serial.baudrate = 9600        # Baud
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout  = 1
        self.instrument.close_port_after_each_call = True
        self.instrument.clear_buffers_before_each_transaction = True

        self.T_AMB_REGISTER = 256
        self.T_EV_REGISTER = 257
        self.T_SET_REGISTER = 768
        self.DELTAT_SET_REGISTER = 769
        self.FAN_SET_REGISTER = 777
        self.IO_STATUS_REGISTER = 1280
        self.ALARM_STATUS_REGISTER = 1282
        self.DEVICE_STATUS_REGISTER = 1536
        self.STANDBY_MASK = 0x1
        self.DEFROST_MASK = 0x4

    def getRegister(self,register):
        try:
            value=self.instrument.read_register(register)
            return value
        except IOError:
            print("Failed to read from instrument")

    def setRegister(self,register,value):
        try:
            write_register(register, value, functioncode=6)
            return 0
        except IOError:
            print("Failed to write to instrument")
            return -1

    def getAmbientTemperature(self):
        value=self.getRegister(self.T_AMB_REGISTER)
        if (value<32768):
            return value*0.1
        else:
            return (value-65536)*0.1

    def getEvaporatoTemperature(self):
        value=self.getRegister(self.T_SET_REGISTER)
        if (value<32768):
            return value*0.1
        else:
            return (value-65536)*0.1

    def getTargetTemperature(self):
        value=self.getRegister(self.T_SET_REGISTER)
        if (value<32768):
            return value*0.1
        else:
            return (value-65536)*0.1

    def setTargetTemperature(self,value):
        if (value<0):
            value=65536-int(value*10)
        else:
            value=value*10
        r=self.setRegister(self.T_SET_REGISTER,value)
        return r

    def getDeltaTemperature(self):
        value=self.getRegister(self.DELTAT_SET_REGISTER)
        return value*0.1

    def setDeltaTemperature(self,value):
        if (value<0):
            value=0.2
        value=value*10
        r=self.setRegister(self.T_SET_REGISTER,value)
        return r

    def getFanSettings(self):
        value=self.getRegister(self.FAN_SET_REGISTER)
        return value

    def setFanSettings(self,value):
        if (value<0):
            value=0
        if (value>1):
            value=1
        r=self.setRegister(self.FAN_SET_REGISTER,value)
        return r

    def getDeviceStatus(self):
        value=self.getRegister(self.DEVICE_STATUS_REGISTER)
        return value

    def getAlarmStatus(self):
        value=self.getRegister(self.ALARM_STATUS_REGISTER)
        return value

    def getIOStatus(self):
        value=self.getRegister(self.IO_STATUS_REGISTER)
        return value

    def start(self):
        status=getDeviceStatus()
        if (status&self.STANDBY_MASK): # 1 means standby
            #put on 
            value=self.STANDBY_MASK<<8
            r=self.setRegister(self.DEVICE_STATUS_REGISTER,value)
            return r
        else:
            return 0 #already on

    def standby(self):
        status=getDeviceStatus()
        if not (status&self.STANDBY_MASK): # 0 means on
            #standby bit and modify bit on 
            value=self.STANDBY_MASK<<8|self.STANDBY_MASK
            r=self.setRegister(self.DEVICE_STATUS_REGISTER,value)
            return r
        else:
            return 0 #already on

    def defrost(self):
        status=getDeviceStatus()
        if not (status&self.DEFROST_MASK): # checking if already defrost is on
            #put on 
            value=self.DEFROST_MASK<<8|self.DEFROST_MASK
            r=self.setRegister(self.DEVICE_STATUS_REGISTER,value)
            return r
        else:
            return 0 #already on

