#!/usr/bin/python
import time
import os
import sys

def read(filename):
    """Reads data from a file and returns the data."""
    tempFile = open(filename)
    data = tempFile.read()
    tempFile.close
    return data
def getMACAddr(interface):
    """Retrieves the hardware address from the interface provided. If the method
    fails to retrieve the MAC (Media Access Control) address from the given
    interface, then the MAC address for the eth0 interface will be returned."""
    MAC_ADDRESS_eth0 = '/sys/class/net/eth0/address'
    filename = '/sys/class/net/' + interface + '/address'
    try:
        macAddress = read(filename)
    except:
        macAddress = read(MAC_ADDRESS_eth0)
    print 'Reading MAC Adress...: ', macAddress.strip()
    return macAddress.strip()
def readTemperature(filename):
    """Reads the temperature in degrees celcius from a file.
    It returns the recorded time of the temperature along with the
    temperature in degrees celcius and farenheit.
    A TempSensorError can be thrown in two cases:
    1) if the temperature sensor is disconnected and the file that contains
    the temperature does not exist.
    2) If the file exists but the temperature sensor was quickly disconnected
    after the file was read."""
    print 'Reading temperature...'
    try :
        # The temperature sensor can be disconnected and thus the file
        # containing the temperature would not exist
        data = read(filename)
    except IOError:
        raise TempSensorError('The temperature sensor is disconected.')
    else:
        # [time, date, timezone]
        timeDateZone = time.strftime('%X %x %Z').split()
        # A TempSensorError can be thrown if the file containig the temperature
        # does not have valid data
        celcius = __parseTemperature(data)
        farenheit = round(celcius * 9.0 / 5.0 + 32.0, 3)
        return (timeDateZone, celcius, farenheit)
def __parseTemperature(data):
    """Parses the temperature in degreees celcius from a string.
    The string contains the following informattion in two lines:
    1) the cycle redundancy check (CRC)
    2) the temperature in celcius.
    If the CRC is 00, then the temperature sensor is discconected and a
    TempSensorError is thrown; otherwise, the temperature readings should
    be fine."""
    data = data.split('\n')
    crc = data[0].find('crc=00')
    celcius = data[1].split('t=')
    if crc != -1:
        raise TempSensorError('The temperature sensor is discconected.')
    return float(celcius[1]) / 1000
class TempSensorError(Exception):
    def __init__(self, message):
        self.message = message
