import bdl
import adafruit_sdcard
import storage
import digitalio
import board
import time


spi = board.SPI()
cs = digitalio.DigitalInOut(board.SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
time.sleep(1)
storage.mount(vfs, "/sd")

if False:  # change to True if you want to set the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2023, 6,   1,   12,   35, 2,   0,    -1,   -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    print("Setting time to:", t)  # uncomment for debugging
    bdl.rtc.datetime = t
    print()

while True:
    # open file for append
    with open("/sd/dateTime.txt", "a") as f:
        RTC = bdl.rtc.datetime
        temp = (bdl.rtc.temperature * 1.8) + 32
        f.write(str("Date: {} {}/{}/{}".format(
                bdl.days[int(RTC.tm_wday)], RTC.tm_mon, RTC.tm_mday, RTC.tm_year
            )) + " " + str("Time: {}:{:02}:{:02}".format(RTC.tm_hour, RTC.tm_min, RTC.tm_sec) +" "+ "Temp: f°%0.1f\n" % temp))
        
    # file is saved
    time.sleep(60)
