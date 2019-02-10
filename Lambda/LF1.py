import boto3
import json
def lambda_handler(event, context):
    # TODO implement
    print(event);
    currIntent = event["currentIntent"]["name"];
    print(currIntent);

    if (currIntent == "ThankYouIntent"):

        result = {

        "dialogAction": {
            "fulfillmentState": "Fulfilled",
            "type": "Close", "message":
                {
                    "contentType": "PlainText",
                    "content": "Bye, see you soon!"
                }

        }
        }
        return result

    if (currIntent == "GreetingIntent"):

        result = {
        "sessionAttributes": {},
        "dialogAction": {
            "fulfillmentState": "Fulfilled",
            "type": "Close", "message":
                {
                    "contentType": "PlainText",
                    "content": "Hey, how may I help you!"
                }

        }
        }
        return result

    if (currIntent == "DiningSuggestionsIntent"):
      slotValue = event["currentIntent"]["slots"];
      location = slotValue["Location"];
      cuisine = slotValue["Cuisine"];
      dining_time = slotValue["Dining_Time"];
      number_of_people = slotValue["Number_of_people"];
      Phone_Number = slotValue["Phone_Number"];
      print(location, cuisine,dining_time,number_of_people,Phone_Number)
      sqs = boto3.resource('sqs')
      queue = sqs.get_queue_by_name(QueueName='DiningQueue')
      string_to_send_sqs={'Location':location,'Cuisine':cuisine,'Dining_time':dining_time,'Number_of_people':number_of_people,'Phone_Number':Phone_Number};
      queue.send_message(MessageBody=json.dumps(string_to_send_sqs))
      result = {
        "sessionAttributes": {},
        "dialogAction": {
        "fulfillmentState": "Fulfilled",
        "type": "Close", "message":
            {
                "contentType": "PlainText",
                "content": "Thanks for your order!"
            }
            }
      }

      return result
