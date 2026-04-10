import boto3
import csv
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('StudentGrades')
    
    try:
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']
        logger.info(f"Processing file: {file_key} from bucket: {bucket_name}")

        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        
        csv_content = response['Body'].read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(csv_content)
        
        for row in csv_reader:
            table.put_item(Item=row)
            
        logger.info("Successfully processed CSV and wrote to DynamoDB.")
        return {'statusCode': 200, 'body': 'Data ingestion complete!'}
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return {'statusCode': 500, 'body': 'Error processing file.'}
