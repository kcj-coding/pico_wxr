# code adapted from https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/examples/pico_explorer/weatherstation_BME280.py
import time
import os
from breakout_bme280 import BreakoutBME280
from pimoroni_i2c import PimoroniI2C
from pimoroni import PICO_EXPLORER_I2C_PINS
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER

# set up the hardware
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)
i2c = PimoroniI2C(**PICO_EXPLORER_I2C_PINS)
bme = BreakoutBME280(i2c, address=0x76)

# lets set up some pen colours to make drawing easier
TEMPCOLOUR = display.create_pen(0, 0, 0)  # this colour will get changed in a bit
HUMIDCOLOUR = display.create_pen(0, 0, 0)  # this colour will get changed in a bit
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
RED = display.create_pen(255, 0, 0)
GREY = display.create_pen(125, 125, 125)
GREEN = display.create_pen(0, 255, 0)
BLUE = display.create_pen(0, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
LIGHT_BLUE = display.create_pen(0, 255, 255)


# converts the temperature into a barometer-type description and pen colour
def describe_temperature(temperature):
    global TEMPCOLOUR
    if temperature < 10:
        description = "very cold"
        TEMPCOLOUR = LIGHT_BLUE
    elif 10 <= temperature < 20:
        description = "cold"
        TEMPCOLOUR = BLUE
    elif 20 <= temperature < 25:
        description = "temperate"
        TEMPCOLOUR = GREEN
    elif 25 <= temperature < 30:
        description = "warm"
        TEMPCOLOUR = YELLOW
    elif temperature >= 30:
        description = "very warm"
        TEMPCOLOUR = RED
    else:
        description = ""
        TEMPCOLOUR = BLACK
    return description

# converts pressure into barometer-type description
def describe_pressure(pressure):
    if pressure < 970:
        description = "storm"
    elif 970 <= pressure < 990:
        description = "rain"
    elif 990 <= pressure < 1010:
        description = "change"
    elif 1010 <= pressure < 1030:
        description = "fair"
    elif pressure >= 1030:
        description = "dry"
    else:
        description = ""
    return description


# converts humidity into good/bad description
def describe_humidity(humidity):
    global HUMIDCOLOUR
    if 40 < humidity < 60:
        description = "good"
        HUMIDCOLOUR = GREEN
    else:
        description = "bad"
        HUMIDCOLOUR = RED
    return description

Lognbr=0
try:
    os.remove("logfile.csv")
except:
    pass

while True:
    Lognbr=Lognbr+1
    display.set_pen(BLACK)
    display.clear()

    # read the sensors
    temperature, pressure, humidity = bme.read()
    # pressure comes in pascals which is a reight long number, lets convert it to the more manageable hPa
    pressurehpa = pressure / 100

    # draw a thermometer/barometer thingy
    #display.set_pen(GREY)
    #display.circle(190, 190, 40)
    #display.rectangle(180, 45, 20, 140)

    # switch to red to draw the 'mercury'
    #display.set_pen(RED)
    #display.circle(190, 190, 30)
    #thermometerheight = int(120 / 30 * temperature)
    #if thermometerheight > 120:
    #    thermometerheight = 120
    #if thermometerheight < 1:
    #    thermometerheight = 1
    #display.rectangle(186, 50 + 120 - thermometerheight, 10, thermometerheight)
    display.set_pen(WHITE)
    display.text(str(round(temperature,3))+"C", 170, 10, 240, 2)
    display.text(str(round(pressurehpa,2)) + 'hPa', 140, 25, 240, 2)
    display.text(str(round(humidity,2)) + '%', 170, 40, 240, 2)

    # drawing the temperature text
    display.set_pen(WHITE)
    display.text("temperature:", 10, 10, 240, 2)
    display.set_pen(TEMPCOLOUR)
    display.text('{:.1f}'.format(temperature) + 'C', 10, 30, 240, 4)
    display.set_pen(WHITE)
    display.text("---"+describe_temperature(temperature), 10, 60, 240, 2)

    # and the pressure text
    display.text("pressure:", 10, 90, 240, 2)
    display.text('{:.0f}'.format(pressurehpa) + 'hPa', 10, 110, 240, 4)
    display.text("---"+describe_pressure(pressurehpa), 10, 140, 240, 2)

    # and the humidity text
    display.text("humidity:", 10, 170, 240, 2)
    display.set_pen(HUMIDCOLOUR)
    display.text('{:.0f}'.format(humidity) + '%', 10, 190, 240, 4)
    display.set_pen(WHITE)
    display.text("---"+describe_humidity(humidity), 10, 220, 240, 2)
    
    display.text(("Runtime:"),100,190,240,3)
    display.text(str(round(Lognbr,2)),130,215,240,3)
    #display.text("Runtime_"+str(round(Lognbr/18,2)*100),100,220,140,2)
    
    logf = open("logfile.csv","a")
    try:
            logf.write(str(temperature))
            logf.write(",")
            logf.write(str(humidity))
            logf.write(",")
            logf.write(str(pressurehpa))
            logf.write(",")
            logf.write(str(Lognbr))
            logf.write("\r\n")
    except OSError:
            try:
                os.remove("logfile.csv")
            except:
                pass
            print("Disk full?") # shouldn't occur
    logf.close()

    # time to update the display
    display.update()

    # waits for 1 second and clears to BLACK
    time.sleep(1)
