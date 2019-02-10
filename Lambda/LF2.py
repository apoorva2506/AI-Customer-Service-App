import http.client
import json
import urllib
import boto3
import datetime
import time
from botocore.vendored import requests
import http.client
import base64
import json
import boto3
import decimal

def lambda_handler(event, context):
    sqs=boto3.resource('sqs')
    queue=sqs.get_queue_by_name(QueueName='DiningQueue')
    for message in queue.receive_messages():
        final_string=json.loads(message.body)
        location = final_string['Location']
        cuisine = final_string['Cuisine']
        dining_time = final_string['Dining_time']
        no_of_people = final_string['Number_of_people']
        phone_number = final_string['Phone_Number']

        message.delete()
        print('deleted')

        headers = {'Authorization':'Bearer 9zufu4z0309-nY2mBhXSm8GZEctBZGrtIoR9eqt9sxVv7h9NfBXMsNySKf1p3Y_RHF4vg3nBmBBfxS8SPqOAeIcOKNMIJQf-MQmlyUhbQxoX2dSZatl9sttTKZDnW3Yx',}
        client = boto3.client('dynamodb')
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table= dynamodb.Table('DiningsuggestionTable')

        # try:
        conn = http.client.HTTPSConnection("api.yelp.com")
        url = "https://api.yelp.com/v3/businesses/search?term=" + str(cuisine) + "&location=" + str(location)
        conn.request("GET",url, headers = headers)
        response=conn.getresponse()
        data=response.read()
        data = json.loads(data.decode("utf-8"))
        restaurant_yelpdata =data["businesses"]
        restaurantList=[];
        addresslist = []
        restaurantListLocation=[];
        for i in range(len(restaurant_yelpdata)):
            restaurant = restaurant_yelpdata[i]
            id = restaurant['id']
            Cuisine = restaurant['categories'][0]['title']
            Rating = decimal.Decimal(restaurant['rating'])
            NumberOfReviews = restaurant['review_count']
            Zipcode=restaurant['location']['zip_code']
            name = restaurant['name']
            address = restaurant['location']['address1']
            if i<3:
                restaurantList.append(name)
                addresslist.append(address)
                # restaurantListLocation.append(Zipcode)
            print(id, Cuisine, Rating, NumberOfReviews, Zipcode, name)
            response=table.put_item(Item={"categories":Cuisine,"id":id,"Rating":Rating,"review_count":NumberOfReviews,\
                                         "Zip Code":Zipcode,"Name":name})
            print(response)

        conn.close()

        stringToOutput=""
        for j in range(3):
            stringToOutput += " " +restaurantList[j] + " " + addresslist[j] + "\n"

        string_toSend = "Hello! Here are my "+ cuisine + " restaurant suggestions for " + no_of_people + " people, for " + dining_time + ": \n"
        string_toSend=string_toSend+stringToOutput
        client=boto3.client('sns')
        # client.subscribe(TopicArn = 'arn:aws:sns:us-east-1:995739821424:DiningMessages',Protocol='SMS',Endpoint=phone_number)
        client.publish(Message=string_toSend, PhoneNumber=phone_number)

    # except:
        #  print("not working")
