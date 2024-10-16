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
from datetime import datetime


appCancelFundInvesting = APIRouter()


@appCancelFundInvesting.post("/canceledBodingFund/")
async def canceledBodingFund(Id:str):
    
    try:
        print(Id)
        fundsInvestment = connection("fundsInvestment")
       
        fundsInvestmentResponse = fundsInvestment.query(
                IndexName='idIndex',  # Nombre del índice secundario
                KeyConditionExpression=Key('id').eq(Id)
            )
        
        # Verifica si el ítem fue encontrado
        item = fundsInvestmentResponse.get('Items')
        fundsInvestmentConsult = item[0]
        
        # Actualización del status de un fondo de inversión
        updateStatusFundsInvestment = fundsInvestment.update_item(
            Key={
                'id': Id
            },
            UpdateExpression="SET #status = :new_status",
            ExpressionAttributeNames={
                '#status': 'status'  # Alias para la palabra reservada
            },
            ExpressionAttributeValues={
                ':new_status': 'Inactive'  # o cualquier otro valor que necesites
            }
        )
        
        # Acceder a la tabla fondo de inversión para adquirir el id
        accountMonetaryTable = connection("AccountMonetary")
        # Obtener los datos del fondo de inversión
        responseAccountMonetary = accountMonetaryTable.query(
                IndexName='userIdIndex',  # Nombre del índice secundario
                KeyConditionExpression=Key('userId').eq(fundsInvestmentConsult["userId"])
            )
        # Obtener cuenta del cliente
        accountMonetary = responseAccountMonetary.get('Items')
        accountMonetaryConsult = accountMonetary[0]
       
        # Actualización del monto
        updateAccountMonetary = accountMonetaryTable.update_item(
            Key={
                'id': accountMonetaryConsult['id']
            },
            UpdateExpression="set amount = :amount",
            ExpressionAttributeValues={':amount': accountMonetaryConsult['amount']+fundsInvestmentConsult["investedAmount"]},
            ReturnValues="UPDATED_NEW"
        )
        
        # Acceder a la tabla User para adquirir el id
        usersTable = connection("Users")
        # Obtener usuario item
        useResponse = usersTable.query(
                IndexName='idIndex',  # Nombre del índice secundario
                KeyConditionExpression=Key('id').eq(fundsInvestmentConsult["userId"])
            )
         # Verifica si el ítem fue encontrado
        User = useResponse.get('Items')
        userConsult = User[0]
        
        #obtener dataos de los fondos
        fundsTable = connection("Funds")
        # Obtener usuario item
        fundsResponse = fundsTable.query(
                IndexName='idIndex',  # Nombre del índice secundario
                KeyConditionExpression=Key('id').eq(fundsInvestmentConsult['fundId'])
            )
         # Verifica si el ítem fue encontrado
        funds = fundsResponse.get('Items')
        fundsConsult = funds[0]
        
        # Datos para enviar mensaje o notificación
        client = userConsult['fullName']
        nameFund = fundsConsult["name"]
        clintPhone = userConsult['phoneNumber']
        FundNumberUnique = fundsInvestmentConsult["uniqueNumber"]
        # Enviar notificación
        if fundsInvestmentConsult['notificationPreferences'] == "email":
            # Enviar correo de notificación
            message = f"Haz cancelado su fondo de inversión {nameFund} N° {FundNumberUnique}"
            sendEmail(userConsult["fullName"], f'Cancelación de Fondo de Inversión {nameFund}', message)
        else:
            # Enviar msm de notificación
            message = f"¡Hola {client}! btg Pactual te informa que haz cancelado su fondo de inversión {nameFund} N° {FundNumberUnique}"
            phoneNumber = f"+57{clintPhone}"
            sendMSM(message, phoneNumber)
        
        #creación de ID
        idItem = str(ObjectId())
        notificationId = str(ObjectId())
        # Llamar tabla "Notification"
        tableNotification = connection("Notifications")
        # creaar datos para las notificaciones
        newNotifcation = {
            "id": notificationId,
            "transactionId": idItem,
            "medium": fundsInvestmentConsult['notificationPreferences'],
            "sendDate":  datetime.now().isoformat()
            
        }
        tableNotification.put_item(Item=newNotifcation)
        # Tomamos datos para registar la transacciones relaizadas por el usuario
        tableTransaction = connection("Transactions")
        fundsConsult['minimumAmount'] = float(fundsConsult['minimumAmount'])
        fundsInvestmentConsult['investedAmount'] = float(fundsInvestmentConsult['investedAmount'])
        newTransaction = {
            "id": str(ObjectId()),
            'bondingFundId': idItem,
            'fundId': fundsInvestmentConsult['fundId'],
            'type': "Cancelación",
            'amount': 0,
            'date': datetime.now().isoformat(),
            'status':"completado",
            'uniqueNumber': FundNumberUnique,
            "fundsInvestment":{"notification":fundsInvestmentConsult["notificationPreferences"]},
            "fund":{"name":fundsConsult["name"],"category":fundsConsult["category"]}
            
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

  