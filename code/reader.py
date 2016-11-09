#!/usr/bin/python
import time
import os
import sys

MAC_ADDRESS_eth0 = '/sys/class/net/eth0/address'

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
    filename = '/sys/class/net/' + interface + '/address'
    try:
        macAddress = read(filename)
    except:
        macAddress = read(MAC_ADDRESS_eth0)
    return macAddress
def readTemperature(filename):
    """Reads the temperature in degrees celcius from a file.
    It returns the recorded time of the temperature along with the
    temperature in degrees celcius and farenheit."""
    data = read(filename)
    currentTime = time.strftime('%x %X %Z')
    celcius = __parseTemperature(data)
    farenheit = round(celcius * 9.0 / 5.0 + 32.0, 3)
    return (currentTime, celcius, farenheit)
def __parseTemperature(data):
    """Parses the temperature in degreees celcius from a string.
    The string contains the following informattion in two lines:
    1) the cycle redundancy check (CRC)
    2) the temperature in celcius.
    If the CRC is 00, then the temperature sensor is discconected;
    otherwise, the temperature readings should be fine."""
    data = data.split('\n')
    checksum = data[0].find('crs=00')
    celcius = data[1].split('t=')
    if checksum == 'crc=00':
        raise TempSensorException('The temperature sensor is discconected.')
    return float(celcius[1]) / 1000
class TempSensorException(Exception):
    def __init__(self, message):
        self.message = message
