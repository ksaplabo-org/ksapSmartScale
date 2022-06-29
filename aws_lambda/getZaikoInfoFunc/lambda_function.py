import os
import json
import boto3
import datetime
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')                   #Dynamodbアクセスのためのオブジェクト取得

def lambda_handler(event, context):	                    #Lambdaから最初に呼びされるハンドラ関数

    try:
        if event['body-json']['data-type'] == 'zaiko-master':
            table = dynamodb.Table("ksap-zaiko")          
            scanData = table.scan()

        elif event['body-json']['data-type'] == 'zaiko-harai':
            now_dt = datetime.datetime.now() + datetime.timedelta(hours=9)
            st_dt = now_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            ed_dt = (now_dt - datetime.timedelta(seconds=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
            
            table = dynamodb.Table("ksap-zaiko-harai")
            scanData = table.scan(
                FilterExpression = Attr('update_dt').between(ed_dt ,st_dt)
                )
            if scanData['Count'] > 0:
                scanData['Items'] = sorted(scanData['Items'], key=lambda x: x['datetime'] ,reverse=True)

        items=scanData['Items']
        print(items)
        return scanData
            
    except Exception as e:
        print("Error Exception.")
        print(e)