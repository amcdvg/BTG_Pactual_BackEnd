from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field, EmailStr
from Tools.passwordHashed import hashPasswordSha256
from Data.data import connection
from Model.model import User
from bson import ObjectId
from boto3.dynamodb.conditions import Key
from fastapi.responses import JSONResponse
from Tools.convertDecimalFloat import convertDecimalFloat

appBalance = APIRouter()

# consultar todas las transacciones
@appBalance.get("/getBalance/")
async def getBalance():
    try:
        Balancess = []
        BalancessTable = connection("AccountMonetary")
        # Realiza la operación de scan con paginación
        response = BalancessTable.scan()
        Balancess.extend(response.get('Items', []))

        # Maneja la paginación
        while 'LastEvaluatedKey' in response:
            response =  BalancessTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            Balancess.extend(response.get('Items', []))

        if not Balancess:
            raise HTTPException(status_code=404, detail="No items found")
        
        # Convierte Decimal a float
        Balance =  convertDecimalFloat(Balancess)
        
        # Acceder a la tabla User para adquirir el id
        usersTable = connection("Users")
        # Obtener los datos del usuario
        responseUser = usersTable.query(
                IndexName='EmailIndex',  # Nombre del índice secundario
                KeyConditionExpression=Key('email').eq(Balance['userId'])
            )
        # Obtener usuario
        user = responseUser.get('Items')
        userConsult = user[0]
        
        dataResponse ={
            "name":userConsult['fullName'],
            "email":userConsult['email'],
            "phoneNumbeer":userConsult['phoneNumber'],
            "Balance":Balance["amount"],
            "IdBalance":Balance["id"]
            
        }
        
        #return Balancess
       
        return JSONResponse(
                status_code=200,
                content={
                    "status": 200,
                    "message": "Operation was successful",
                    "data": dataResponse
                }
            )
    except Exception as e:
        # Manejar cualquier error inesperado
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")