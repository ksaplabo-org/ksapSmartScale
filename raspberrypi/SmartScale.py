from bluepy import btle
import re
import math
import datetime 
import time

SCAN_TIMEOUT = 3.0

class SmartScale:
    def __init__(self):
        self.__zaikoTbl = []

    def _getWeight(self ,adServiceData):
        result = False
        weight = 0
        for (adTypeCode, description, valueText) in adServiceData:
            if description == "16b Service Data":
                try:
                    w_tmp = re.split('(..)',valueText)[1::2]
                    w_tmp_str = ""
                    for i in range(2,9):
                        w_tmp_str = w_tmp_str + chr(int('0x' + str(w_tmp[i]),0))
                    weight = float(w_tmp_str.replace(' ',''))
                    result = True

                except Exception as e:
                    print("Exception in _getWeight cause by " & e)

        return result ,weight

    def _getZaikosu(self ,zaiko ,scaleWeight):
        if scaleWeight <= zaiko['weight_box']:
            weight = 0
            zaikosu = 0
        else:
            weight = scaleWeight - zaiko['weight_box']
            zaikosu = math.floor((weight / zaiko['weight_one']) + 0.5)
        return zaikosu

    def updateZaiko(self ,haraiList):
        for harai in haraiList:
            for zaiko in self.__zaikoTbl:
                if zaiko['id'] == harai['zaiko']['id']:
                    zaiko['weight'] = harai['scaleWeight']
                    zaiko['zaikosu'] = harai['zaikosu']
                    break

    def getHarai(self):

        # BLEデバイスをスキャン
        scanner = btle.Scanner(0)
        devices = scanner.scan(SCAN_TIMEOUT)

        haraiList = []
        for device in devices:
            adServiceData = device.getScanData()
            for row in self.__zaikoTbl:
                if device.addr == row['addr']:
                    result ,weight = self._getWeight(adServiceData)
                    if result == True:
                        zaikosu = self._getZaikosu(row ,weight)
                        if zaikosu != row['zaikosu']:
                            dt = datetime.datetime.now()
                            haraiList.append(
                                {"zaiko":row, 
                                "datetime":dt.strftime('%Y/%m/%d %H:%M:%S') ,
                                "scaleWeight":weight,
                                "zaikosu":zaikosu ,
                                "haraisu":(row['zaikosu'] - zaikosu)
                                })
                        print("packet recieved!")
                    else:
                        print("cannot recieve beacon(no packet)")
                    break

        scanner.clear()
        time.sleep(3)

        return haraiList

    def regist(self ,zaikolist):
        for zaiko in zaikolist:
            self.__zaikoTbl.append(zaiko)
