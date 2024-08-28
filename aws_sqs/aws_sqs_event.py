import boto3

class AwsSqsEvent:

    def __init__(self, queue_url, region) -> None:
        self.sqs_client = boto3.client("sqs", region_name=region)
        self.queue_url = queue_url

    def delete_message(self, message):
        self.sqs_client.delete_message(
                QueueUrl=self.queue_url, ReceiptHandle=message["ReceiptHandle"]
            )
    def receive_message(self):
        return self.sqs_client.receive_message(
            QueueUrl=self.queue_url,
            AttributeNames=["All"],
            MaxNumberOfMessages=10,
            MessageAttributeNames=["All"],
            VisibilityTimeout=30,
            WaitTimeSeconds=20,
        )