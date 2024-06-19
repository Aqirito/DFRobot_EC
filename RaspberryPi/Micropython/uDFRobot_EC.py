import machine

_kvalue        = 1.0
_kvalueLow     = 1.0
_kvalueHigh    = 1.0

class DFRobot_EC():
    def begin(self):
        global _kvalueLow
        global _kvalueHigh
        try:
            with open('ecdata.py','r') as f:
                kvalueLowLine  = f.readline()
                kvalueLowLine  = kvalueLowLine.strip('kvalueLow=')
                _kvalueLow     = float(kvalueLowLine)
                kvalueHighLine = f.readline()
                kvalueHighLine = kvalueHighLine.strip('kvalueHigh=')
                _kvalueHigh    = float(kvalueHighLine)
        except:
            print("ecdata.py ERROR ! Reset to default parameters")
            self.reset()
    def readEC(self,voltage,temperature):
        global _kvalueLow
        global _kvalueHigh
        global _kvalue
        rawEC = 1000*voltage/820.0/200.0
        valueTemp = rawEC * _kvalue
        if(valueTemp > 2.5):
            _kvalue = _kvalueHigh
        elif(valueTemp < 2.0):
            _kvalue = _kvalueLow
        value = rawEC * _kvalue
        value = value / (1.0+0.0185*(temperature-25.0))
        return value
    def calibration(self,voltage,temperature):
        rawEC = 1000*voltage/820.0/200.0
        print(rawEC, voltage, temperature)
        if (rawEC>0.9 and rawEC<1.9):
            compECsolution = 1.413*(1.0+0.0185*(temperature-25.0))
            KValueTemp = 820.0*200.0*compECsolution/1000.0/voltage
            round(KValueTemp,2)
            print(">>>Buffer Solution:1.413us/cm")
            f=open('ecdata.py','r')
            flist=f.readlines()
            flist[0]='kvalueLow='+ str(KValueTemp) + '\n'
            f=open('ecdata.py','w')
            f.write(''.join(flist))
            f.close()
            print(">>>EC:1.413us/cm Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds")
            machine.reset()
        elif (rawEC>9 and rawEC<16.8):
            compECsolution = 12.88*(1.0+0.0185*(temperature-25.0))
            KValueTemp = 820.0*200.0*compECsolution/1000.0/voltage
            print(">>>Buffer Solution:12.88ms/cm")
            f=open('ecdata.py','r')
            flist=f.readlines()
            flist[1]='kvalueHigh='+ str(KValueTemp) + '\n'
            f=open('ecdata.py','w')
            f.write(''.join(flist))
            f.close()
            print(">>>EC:12.88ms/cm Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds")
            machine.reset()
        else:
            print(">>>Buffer Solution Error Try Again<<<")
            machine.reset()
    def reset(self):
        _kvalueLow              = 1.0;
        _kvalueHigh             = 1.0;
        try:
            f=open('ecdata.py','r')
            flist=f.readlines()
            flist[0]='kvalueLow=' + str(_kvalueLow)  + '\n'
            flist[1]='kvalueHigh='+ str(_kvalueHigh) + '\n'
            f=open('ecdata.py','w')
            f.write(flist)
            f.close()
            print(">>>Reset to default parameters<<<")
            machine.reset()
        except:
            f=open('ecdata.py','r')
            flist=f.readlines()
            flist   ='kvalueLow=' + str(_kvalueLow)  + '\n'
            flist  +='kvalueHigh='+ str(_kvalueHigh) + '\n'
            f=open('ecdata.py','w')
            f.write(''.join(flist))
            f.close()
            print(">>>Reset to default parameters<<<")
            machine.reset()