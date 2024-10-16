from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from Data.data import connection
from Model.model import BondingFund
from bson import ObjectId
from boto3.dynamodb.conditions import Key
from bson import ObjectId
from fastapi.responses import JSONResponse
from utils.emails.sendEmail import sendEmail
from utils.msm.sendMsm import sendMSM
from hashlib import sha256
import re



appFundInvesting = APIRouter()


def getNumberUnique(fundId, clientId, transactionId):
    # Combinar los IDs
    combinacion = f"{fundId}{clientId}{transactionId}"
    # Generar el hash SHA-256
    hashValue = sha256(combinacion.encode()).hexdigest()
    # Extraer solo los dígitos del hash
    digits = re.sub(r'\D', '', hashValue)  # Eliminar todo lo que no sean dígitos
    # Asegurarse de que tenga 12 dígitos (usar los primeros 12 o rellenar con ceros si es necesario)
    uniqueNumber = (digits[:12] + '000000000000')[:12]  # Completar con ceros si es necesario
    return uniqueNumber
    
# Registrar un nuevo Fondo
@appFundInvesting.post("/vinculatedBodingFund/")
async def vinculatedBodingFund(Account: BondingFund, email:str, fund:str):
    print(BondingFund)
    try:
        # Acceder a la tabla User para adquirir el id
        usersTable = connection("Users")
        # Obtener los datos del usuario
        responseUser = usersTable.query(
                IndexName='EmailIndex',  # Nombre del índice secundario
                KeyConditionExpression=Key('email').eq(email)
            )
        
        # Acceder a la tabla fondo de inversión para adquirir el id
        fundsTable = connection("Funds")
        # Obtener los datos del fondo de inversión
        responseFund = fundsTable.query(
                IndexName='nameIndex',  # Nombre del índice secundario
                KeyConditionExpression=Key('name').eq(fund)
            )
        
        
        
        # Obtener usuario
        user = responseUser.get('Items')
        userConsult = user[0]
        #Obtener fondo de inversión
        fundInvestmentBouding = responseFund.get('Items')
        investmentConsult = fundInvestmentBouding[0]
        
        #Acceder a la tabla de la cuenta de finanza del cliente
        # Acceder a la tabla fondo de inversión para adquirir el id
        accountMonetaryTable = connection("AccountMonetary")
        # Obtener los datos del fondo de inversión
        responseAccountMonetary = accountMonetaryTable.query(
                IndexName='userIdIndex',  # Nombre del índice secundario
                KeyConditionExpression=Key('userId').eq(userConsult["id"])
            )
        # Obtener cuenta del cliente
        accountMonetary = responseAccountMonetary.get('Items')
        accountMonetaryConsult = accountMonetary[0]
       
        # Acceder a la tabla AcccountMonetary de DynamoDB 
        table = connection("fundsInvestment")
        # Validación si se se puede hacer la inversión o no
        if (Account.investedAmount < investmentConsult["minimumAmount"]) or  (accountMonetaryConsult["amount"] < Account.investedAmount):
            return JSONResponse(
                status_code=400,
                content={
                    "status": 400,
                    "message": "Operation wasn’t successful",
                    "data": {"message":"Account insufficient"}
                }
            )
        # Datos para crear un nuevo fondo
        idItem = str(ObjectId())
        notificationId = str(ObjectId())
        FundNumberUnique = getNumberUnique(investmentConsult['id'],userConsult['id'],idItem)
        newAccountMonetary = {
            "id": idItem, 
            "fundId": investmentConsult["id"],
            "investedAmount": Account.investedAmount,
            "bondingDate": Account.bondingDate.isoformat(),
            "userId":userConsult["id"],
            "notificationPreferences":Account.notificationPreferences,
            "notificationId":notificationId,
            "uniqueNumber":FundNumberUnique,
            "status":"Active",
            "fund":{"name":investmentConsult["name"],"category":investmentConsult["category"]}
            
            
        }
        # Insertar en la tabla de DynamoDB
        table.put_item(Item=newAccountMonetary)
        
        # Datos para enviar mensaje o notificación
        client = userConsult['fullName']
        nameFund = investmentConsult["name"]
        clintPhone = userConsult['phoneNumber']
        # Enviar notificación
        if Account.notificationPreferences == "email":
            # Enviar correo de notificación
            message = f"Haz creado un nuevo fondo de inversión {nameFund} N° {FundNumberUnique}"
            sendEmail(userConsult["fullName"], f'Creación de Fondo de Inversión {nameFund}', message)
        else:
            # Enviar msm de notificación
            message = f"¡Hola {client}! btg Pactual te informa que haz creado un nuevo fondo de inversión {nameFund} N° {FundNumberUnique}"
            phoneNumber = f"+57{clintPhone}"
            sendMSM(message, phoneNumber)
            
        # Llamr tabla "Notification"
        tableNotification = connection("Notifications")
        # creaar datos para las notificaciones
        newNotifcation = {
            "id": notificationId,
            "transactionId": idItem,
            "medium": Account.notificationPreferences,
            "sendDate":  Account.bondingDate.isoformat()
            
        }
        tableNotification.put_item(Item=newNotifcation)
        # Actualizar el monto de la cuenta del usuario
        #AccountMonetary
        primaryKey = {
            'id': accountMonetaryConsult['id']
        }
        updateAccountMonetary = accountMonetaryTable.update_item(
            Key=primaryKey,
            UpdateExpression="set amount = :amount",
            ExpressionAttributeValues={':amount': accountMonetaryConsult['amount']-Account.investedAmount},
            ReturnValues="UPDATED_NEW"
        )
        
        # Tomamos datos para registar la transacciones relaizadas por el usuario
        #Notifications
        tableTransaction = connection("Transactions")
        newTransaction = {
            "id": str(ObjectId()),
            'bondingFundId': idItem,
            'fundId': investmentConsult['id'],
            'type': "apertura",
            'amount': Account.investedAmount,
            'date': Account.bondingDate.isoformat(),
            'status':"completado",
            'uniqueNumber': FundNumberUnique,
            "fundsInvestment":{"notification":newAccountMonetary["notificationPreferences"]},
            "fund":{"name":investmentConsult["name"],"category":investmentConsult["category"]}
            
        }
        tableTransaction.put_item(Item=newTransaction)
        
        return JSONResponse(
                status_code=200,
                content={
                    "status": 200,
                    "message": "Operation was successful",
                    "data": newTransaction
                }
            )
    except Exception as e:
        # Manejar cualquier error inesperado
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
