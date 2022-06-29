import SmartScale2 as smsc
from bluepy import btle

smartScale = smsc.SmartScale2()
while True:

    # BLEデバイスをスキャン
    scanner = btle.Scanner(0)
    devices = scanner.scan(3.0)

    haraiList = []
    for device in devices:
        adServiceData = device.getScanData()
        if device.addr == "40:91:51:be:f7:8e": 
            is_servicedata = False
            for (adTypeCode, description, valueText) in adServiceData:
                if description == "16b Service Data":
                    print("packet recieved!")
                    is_servicedata = True
            if is_servicedata == False:
                print("cannot recieve beacon(no packet)")

    scanner.clear()



