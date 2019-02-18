import boto3
import image_to_text
import json

# Create SQS client
sqs = boto3.client('sqs')

SQS_QUEUE_URL = "https://sqs.us-east-2.amazonaws.com/897236463588/demo_doc_input"
queue_url = SQS_QUEUE_URL

# Receive message from SQS queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=[
        'SentTimestamp'
    ],
    MaxNumberOfMessages=1,
    MessageAttributeNames=[
        'All'
    ],
    VisibilityTimeout=0,
    WaitTimeSeconds=0
)
print("Attempting to fetch a message from Queue")
# Check if there are any messages in the Queue
try:
    all_messages = response['Messages']
    message = all_messages[0]
    receipt_handle = message['ReceiptHandle']
    message_body_string = message.get("Body")
    try:
        index_of_key = message_body_string.index("\"key\":\"")+len("\"key\":\"")
        index_of_size = message_body_string.index("\",\"size\":")
        value_of_key = message_body_string[index_of_key:index_of_size]
        print "Found Key: %s" % value_of_key
        try:
            # Fetch image from S3 bucket and perform OCR
            image_to_text.image_recognition(value_of_key)
        except KeyError:
            print("Error in OCR")
    except KeyError:
        print("Error in Extracting file name from message")
    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print('Deleted message')
except KeyError:
    print('Error in receiving message from queue')