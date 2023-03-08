import boto3
from boto3.dynamodb.conditions import Key
import json

def lambda_handler(event, context):
    TABLE = 'dynamodb'
    PARTITION_KEY = 'visitorCount'

    #1. Get and update visitor count
    dynamodb = boto3.resource(TABLE)
    table = dynamodb.Table(PARTITION_KEY)
    
    resp = table.get_item(Key={'cloudResumeChallenge': '1'})
    num = resp['Item']['test']
    num += 1
    table.put_item(Item={'cloudResumeChallenge':'1', 'test':num})

    #2. construct body of response object
    visitorCountResponse = {}
    visitorCountResponse['visitorCount'] = int(num)

    #3. construct http response object and allow CORS
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Headers': 'application/json',
        'Access-Control-Allow-Origin': 'https://www.jakeespinosa.com',
        'Access-Control-Allow-Credentials': True,
        'Access-Control-Allow-Methods': 'OPTIONS,GET'
    }
    
    responseObject['body'] = json.dumps(visitorCountResponse)

    #4. Return the response object
    return responseObject
