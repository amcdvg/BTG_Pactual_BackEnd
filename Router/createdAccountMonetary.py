from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from Data.data import connection
from Model.model import AccountMonetary
from bson import ObjectId
from boto3.dynamodb.conditions import Key
from bson import ObjectId

appAccountMonetary = APIRouter()

# Registrar un nuevo Fondo
@appAccountMonetary.post("/addAccount/")
async def accountMonetary(Account: AccountMonetary, email:str):
    try:
        # Acceder a la tabla User para adquirir el id
        usersTable = connection("Users")
        # Obtener los datos del usuario
        response = usersTable.query(
                IndexName='EmailIndex',  # Nombre del índice secundario
                KeyConditionExpression=Key('email').eq(email)
            )
        # Obtener usuarios y contraseñas encriptadas
        user = response.get('Items')
        userConsult = user[0]
        # Acceder a la tabla AcccountMonetary de DynamoDB 
        table = connection("AccountMonetary")
        # Datos para crear un nuevo fondo
        idItem = str(ObjectId())
        newFunds = {
            "id": idItem, 
            "userId": userConsult["id"],
            "amount": Account.amount,
            "createdAt": Account.createdAt.isoformat(),
        }
        # Insertar en la tabla de DynamoDB
        table.put_item(Item=newFunds)
        return {"status": 200,"message": "Operation was successful", "data": newFunds}
    except Exception as e:
        # Manejar cualquier error inesperado
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
