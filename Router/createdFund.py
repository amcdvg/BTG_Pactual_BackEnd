from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from Data.data import connection
from Model.model import Fund
from bson import ObjectId
from boto3.dynamodb.conditions import Key
from bson import ObjectId

appFunds = APIRouter()

# Registrar un nuevo Fondo
@appFunds.post("/addFund/")
async def fundsItem(funds: Fund):
    try:
        # Acceder a la tabla de DynamoDB
        table = connection("Funds")
        # Datos para crear un nuevo fondo
        idItem = str(ObjectId())
        newFunds = {
            "id": idItem, 
            "name": funds.name,
            "minimumAmount": funds.minimumAmount,
            "category": funds.category,
        }
        # Insertar en la tabla de DynamoDB
        table.put_item(Item=newFunds)
        return {"Fondo": funds.name, "id": idItem}
    except Exception as e:
        # Manejar cualquier error inesperado
        
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
