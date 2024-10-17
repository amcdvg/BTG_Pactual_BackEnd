import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import BotoCoreError, ClientError

# Función Conexión a DynamoDB
def connection(tableName):
    #try:
        # Cargar las variables del archivo .env
        load_dotenv()

        # Acceder a las variables del .env para la conexión de la base de datos
        awsAccessKeyId = os.getenv("AWSACCESSKEYID")
        awsSecretAccessKey = os.getenv("AWSSECRETACCESSKEY")
        awsRegion = os.getenv("AWSREGION")
        # Conexión con AWS
        dynamodb = boto3.resource("dynamodb",
                            aws_access_key_id=awsAccessKeyId,
                            aws_secret_access_key=awsSecretAccessKey)
        
        # Obtener la tabla correspondiente de DynamoDB
        table = dynamodb.Table(tableName)
        # Validar si la tabla existe en DynamoDB (opcional)
        table.load()  # Esto lanzará un error si la tabla no existe
        return table
    #except (BotoCoreError, ClientError) as e:
        # Retorna el mensaje de error relacionado con la conexión a DynamoDB
    #    return {"table": None, "error": f"Error connecting to DynamoDB: {str(e)}"}
    #except Exception as e:
        # Retorna otros errores inesperados
    #    return {"table": None, "error": f"An unexpected error occurred: {str(e)}"}
