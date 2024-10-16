from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field, EmailStr
from Tools.passwordHashed import hashPasswordSha256
from Data.data import connection
from Model.model import User
from bson import ObjectId
from boto3.dynamodb.conditions import Key
from fastapi.responses import JSONResponse
from Tools.convertDecimalFloat import convertDecimalFloat

appgetFundViculate = APIRouter()

# consultar todas las transacciones
@appgetFundViculate .get("/getFundViculate/")
async def getFunds():
    try:
        Transactions = []
        transactionsTable = connection("fundsInvestment")
        # Realiza la operación de scan con paginación
        response = transactionsTable.scan()
        Transactions.extend(response.get('Items', []))

        # Maneja la paginación
        while 'LastEvaluatedKey' in response:
            response =  transactionsTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            Transactions.extend(response.get('Items', []))

        if not Transactions:
            raise HTTPException(status_code=404, detail="No items found")
        
        # Convierte Decimal a float
        Funds =  convertDecimalFloat(Transactions)
        
        
        #return Transactions
       
        return JSONResponse(
                status_code=200,
                content={
                    "status": 200,
                    "message": "Operation was successful",
                    "data": Funds
                }
            )
    except Exception as e:
        # Manejar cualquier error inesperado
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")