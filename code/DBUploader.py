#!/usr/bin/python
import PI
import reader
import sqlite3
import database
from reader import TempSensorError

def main():
    tempFile = '/sys/bus/w1/devices/28-00044a3b10ff/w1_slave'
    interface = 'wlan0'
    try:
        macAddr = reader.getMACAddr(interface)
        place = PI.location[macAddr]
        (timeDateZone, celcius, farenheit) = reader.readTemperature(tempFile)
        database.uploadToDB((timeDateZone, celcius, farenheit), place)
    except KeyError as error:
        print error.message, ': device not registered.'
    except TempSensorError as error:
        print place, ': ', error.message
    except sqlite3.Error as error:
        print place, ': aaa', error.message
    else:
        print 'Success...'
def __getProjectDir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if __name__ == '__main__':
    main()
