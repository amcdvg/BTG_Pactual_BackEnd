from boto3 import resource
import os
from dotenv import load_dotenv


# Función para crear tablas en DynamoDB
def createTable(tableName, partitionKey):
    try:
        # Cargar las variables del archivo .env
        load_dotenv()

        # Acceder a las variables del .env para la conexión de la base de datos
        awsAccessKeyId = os.getenv("AWSACCESSKEYID")
        awsSecretAccessKey = os.getenv("AWSSECRETACCESSKEY")
        awsRegion = os.getenv("AWSREGION")

        dynamodb = resource("dynamodb",
                            aws_access_key_id=awsAccessKeyId,
                            aws_secret_access_key=awsSecretAccessKey)
        table = dynamodb.create_table(
            TableName=tableName,
            KeySchema=[
                {
                    'AttributeName': partitionKey,
                    'KeyType': 'HASH'  # Partition Key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': partitionKey,
                    'AttributeType': 'S'  # String
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Table {tableName} created successfully!")
    except Exception as e:
        print(f"Error creating table {tableName}: {e}")



createTable("fundsInvestment", "id")
