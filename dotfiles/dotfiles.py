#!/usr/bin/python

import sys
import platform
import io
from systems import Systems

def identifySystem():
  global sysName
  supportedPlatforms = [Systems.DARWIN.value, Systems.LINUX.value]
  sysName = platform.system()

  if sysName not in supportedPlatforms:
    print "System not supported!"
    exit(1)
  print "System identified as " + sysName

if __name__ == '__main__':
  identifySystem()
  with io.StringIO() as fileBuffer:
    bashfile.writeHeader(sysName, fileBuffer)
