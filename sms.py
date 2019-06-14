import boto3

client = boto3.client(
    "sns",
    aws_access_key_id="ID",
    aws_secret_access_key="SECRET_KEY",
    region_name="eu-west-1"
)

client.publish(
    PhoneNumber="NUMBER",
    Message="Hello !"
)
