import json
import os
import boto3
from decimal import Decimal

def lambda_handler(event, context):

    try:
        for record in event['Records']:
            #データ取得
            id = record['dynamodb']['NewImage']['id']['S']
            zaikosu =  record['dynamodb']['NewImage']['zaikosu']['N']
            scaleWeight = Decimal(str(record['dynamodb']['NewImage']['scaleWeight']['N']))

            # DynamoDB接続設定
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('ksap-zaiko')
                
            # DynamoDB登録処理
            print("putitem before")
            ret = table.update_item(
                Key={
                    'id': id
                },
                UpdateExpression='SET zaikosu = :zaikosu ,weight = :weight',
                ExpressionAttributeValues={
                    ':zaikosu':zaikosu,
                    ':weight':scaleWeight
                }
            )
            print("putitem after")

    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
        
    return {
        'statusCode': 200,
        'body': ""
    }

#Local Execute
#testdata = {"Records":[{"dynamodb":{"NewImage":{"GetDateTime":{"S":"2021-11-03 16:20:18"},"Temperature":{"N":"20.5"},"Humidity":{"N":"72.3"}}}}]}
#lambda_handler(testdata,"")
