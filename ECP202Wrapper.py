import minimalmodbus
from time import sleep

T_AMB_REGISTER = 256
T_EV_REGISTER = 257
T_SET_REGISTER = 768
DELTAT_SET_REGISTER = 769
FAN_SET_REGISTER = 777

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
        value=self.getRegister(T_AMB_REGISTER)
        if (value<32768):
            return value*0.1
        else:
            return (value-65536)*0.1

    def getEvaporatoTemperature(self):
        value=self.getRegister(T_SET_REGISTER)
        if (value<32768):
            return value*0.1
        else:
            return (value-65536)*0.1

    def getTargetTemperature(self):
        value=self.getRegister(T_SET_REGISTER)
        if (value<32768):
            return value*0.1
        else:
            return (value-65536)*0.1

    def setTargetTemperature(self,value):
        if (value<0):
            value=65536-int(value*10)
        else:
            value=value*10
        r=self.setRegister(T_SET_REGISTER,value)
        return r

    def getDeltaTemperature(self):
        value=self.getRegister(DELTAT_SET_REGISTER)
        return value*0.1

    def setDeltaTemperature(self,value):
        if (value<0):
            value=0.2
        value=value*10
        r=self.setRegister(T_SET_REGISTER,value)
        return r

    def getFanSettings(self):
        value=self.getRegister(FAN_SET_REGISTER)
        return value

    def setFanSettings(self,value):
        if (value<0):
            value=0
        if (value>1):
            value=1
        r=self.setRegister(FAN_SET_REGISTER,value)
        return r


     
