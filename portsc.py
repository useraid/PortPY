#!/bin/python

import sys
import socket as sc
from datetime import datetime as dt

if len(sys.argv) == 3:
    target = sc.gethostbyname(sys.argv[1])
    port = int(sys.argv[2])
else:
    print("Invalid Args")
    sys.exit()

print("scanning "+target+" at "+str(dt.now()))

try:
    # for port in range(50,85):
        s = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        sc.setdefaulttimeout(1)
        result = s.connect_ex((target,port))
        if result == 0:
            print(f"Port {port} is open")
        s.close()

except KeyboardInterrupt:
    print("Exiting")
    sys.exit()