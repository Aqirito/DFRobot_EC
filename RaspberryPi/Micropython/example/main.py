from machine import Pin, ADC
import utime
from uDFRobot_EC import DFRobot_EC

ec = DFRobot_EC()
ec.begin()

adc = ADC(Pin(28, Pin.IN)) # Read Analog Value from a ADC Pin GPIO28
 
while True:
    temperature = 25 # Need to read the water temperature in Celsius
    adc_value_16bit = adc.read_u16()
    adc_value_12bit = adc_value_16bit >> 4  # Convert to 12-bit by shifting right 4 bits
    EC = ec.readEC(adc_value_12bit,temperature)
    print("Temperature:%.1f EC:%.2f ms/cm"%(temperature,EC))
    utime.sleep(0.5)