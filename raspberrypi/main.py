import SmartScale as smsc
import AWSSender as aws
import time

sender = aws.AWSSender()

def getZaiko():
    scales = [{"id":"marble","name":"ビー玉", "addr":"30:c6:f7:22:3b:b2" ,"weight":0 ,"weight_box":57.9,"weight_one":5.4,"zaikosu":0}]
    return scales

smartScale = smsc.SmartScale()
smartScale.regist(getZaiko())
while True:

    haraiList = smartScale.getHarai()

    for harai in haraiList:
        if harai["haraisu"] > 0:
            print(harai["datetime"] + ":" +
                harai["zaiko"]["name"] + " が " + 
                str(harai["haraisu"]) + "個 " +
                "払い出されました。" + 
                "(在庫数：" + str(harai['zaikosu']) + '個)')
        else:
            print(harai["datetime"] + ":" +
                harai["zaiko"]["name"] + " が " + 
                str(abs(harai["haraisu"])) + "個 " + 
                "入庫されました。" + 
                "(在庫数：" + str(harai['zaikosu']) + '個)')

    smartScale.updateZaiko(haraiList)

    sender.putHarai(haraiList)

