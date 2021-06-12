import npyscreen
from ECP202Wrapper import ECP202
import csv
import time

class App(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", ECP202ControlPanel, name="ECP202 Control Panel V1.0 by PM")

class ECP202ControlPanel(npyscreen.ActionForm):
    # Constructor
    def create(self):
        self.OK_BUTTON_TEXT='Apply'
        self.CANCEL_BUTTON_TEXT='Exit'
        self.__class__.CANCEL_BUTTON_BR_OFFSET = (2, 15)

        # Add the TitleText widget to the form
#        self.port = self.add(npyscreen.TitleFilename, name="BOARD       :", value="/dev/ecp202_sn48", editable=False)
        self.port = self.add(npyscreen.TitleFilename, name="CONNECT     :", value="/dev/ttyUSB0", editable=False)
        self.ecp202 = ECP202(self.port.value)
        self.chStatus = not (self.ecp202.getDeviceStatus()&self.ecp202.STANDBY_MASK)
        self.switch = self.add(npyscreen.Checkbox, name = "ON/OFF", scroll_exit=True, rely=5)
        if (self.chStatus):
            self.switch.value=True
        else:
            self.switch.value=False
        self.defrostSwitch = self.add(npyscreen.Checkbox, name = "DEFROST", scroll_exit=True, rely=6)
        self.defrost = (self.ecp202.getDeviceStatus()&self.ecp202.DEFROST_MASK)
        if (self.defrost):
            self.defrostSwitch.value=True
        else:
            self.defrostSwitch.value=False
        self.tset_target=self.ecp202.getTargetTemperature()
        self.tset = self.add(npyscreen.TitleText, name="TSET:", value=str(self.tset_target), rely=8)
        self.tmon = self.add(npyscreen.TitleText, name="T        :", value="", editable=False, rely=11)
        self.status = self.add(npyscreen.TitleText, name="STATUS        :", value="", editable=False)
        self.alarm = self.add(npyscreen.TitleText, name="ALARM         :", value="", editable=False)
        
        self.monitorSwitch = self.add(npyscreen.Checkbox, name = "Write to file", scroll_exit=True, rely=15)
        self.writeToFile = self.monitorSwitch.value
        self.outputFilename = self.add(npyscreen.TitleFilename, name="Output file :", value="test.csv")
#        self.parentApp.setNextForm(None)
        self.counter=0

    def on_ok(self):
        if (float(self.tset.value)>10):
            self.tset.value=str(10)
        if (float(self.tset.value)<-30):
            self.tset.value=str(-30)

        if (abs(float(self.tset.value) - self.tset_target)>0.01):
            r=self.ecp202.setTargetTemperature(float(self.tset.value))
            if (r==0):
                self.tset_target=float(self.tset.value)
            else:
                self.tset.value='Error setting TSET'

        if (self.defrostSwitch.value != self.defrost):
            if (self.defrostSwitch.value):
                r=self.ecp202.defrost()
            if (r==0):
                self.defrost=self.defrostSwitch.value 
            else:
                self.tset.value='Error enabling defrost'

        if (self.switch.value != self.chStatus):
            if (self.switch.value):
                r=self.ecp202.start()
            else:
                r=self.ecp202.standby()
            if (r==0):
                self.chStatus=self.switch.value 
            else:
                self.tset.value='Error switching refrigerator'

        if (self.monitorSwitch.value != self.writeToFile):
            if (self.monitorSwitch.value):
                self.outputFile=open(str(self.outputFilename.value), mode='w+') 
                self.csvWriter = csv.writer(self.outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                self.writeToFile = self.monitorSwitch.value
            else:
                self.writeToFile = self.monitorSwitch.value

    def while_waiting(self):
        if (self.counter%10==0):
            t=self.ecp202.getAmbientTemperature()
            status=self.ecp202.getIOStatus()
            alarm=self.ecp202.getAlarmStatus()
            self.tmon.value="%3.1f C"%(t)
            self.status.value="%d"%(status)
            self.alarm.value="%d"%(alarm)
            self.tmon.display()
            self.status.display()
            self.alarm.display()
            if (self.writeToFile):
                self.csvWriter.writerow([str(int(self.chStatus)),str(self.tset_target),str(t),str(status),str(alarm),str(time.time())])
                self.outputFile.flush()
            self.counter=1
        else:
            self.counter+=1

    def on_cancel(self):
        self.parentApp.setNextForm(None)
        if (self.writeToFile):
            self.outputFile.close()

MyApp = App()
MyApp.run()
