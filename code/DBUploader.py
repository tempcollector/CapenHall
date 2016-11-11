#!/usr/bin/python
import PI
import glob
import reader
import sqlite3
import database
from reader import TempSensorError

def main():
    tempFile = glob.glob('/sys/bus/w1/devices/28-*/w1_slave')[0]
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
        print place, ': ', error.message
    except:
        print tempFile
    else:
        print 'Success...'
if __name__ == '__main__':
    main()
