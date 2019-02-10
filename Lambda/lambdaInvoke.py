import boto3
def lambda_handler(event, context):
    user_id = "userId"
    client = boto3.client('lex-runtime')
    response = client.post_text(
        botName='diningBot',
        botAlias='AABot',
        userId=user_id,
        sessionAttributes={},
        requestAttributes={},
        inputText = event["text"]
    )
    return response["message"]
