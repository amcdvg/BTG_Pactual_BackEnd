from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
import os
from dotenv import load_dotenv
from Tools.passwordHashed import hashPasswordSha256
from Data.data import connection
from Model.model import User
from bson import ObjectId
from boto3.dynamodb.conditions import Key

appUserRegister = APIRouter()

# Registrar un nuevo usuario
@appUserRegister.post("/registerUser/")
async def registerUser(user: User):
    try:
        # Acceder a la tabla de DynamoDB
        table = connection("Users")
        # Verificar si el usuario ya existe
        response = table.query(
            IndexName='EmailIndex',  # Nombre del índice secundario
            KeyConditionExpression=Key('email').eq(user.email)
        )

        items = response.get('Items', [])
        
        if items:
            raise HTTPException(status_code=400, detail="Email already registered")
    
        
        # Crear el nuevo usuario con la contraseña cifrada
        hashed_password = hashPasswordSha256(user.hashedPassword)  # Hasheamos la contraseña aquí
        newUser = {
            "id": str(ObjectId()), 
            "email": user.email,
            "hashedPassword": hashed_password,
            "fullName": user.fullName,
            "phoneNumber": user.phoneNumber,
            "isActive": user.isActive,
            "isSuperuser": user.isSuperuser,
            "createdAt": user.createdAt.isoformat()  # Usar formato ISO 8601
        }
        
        # Insertar en la tabla de DynamoDB
        table.put_item(Item=newUser)
        
        return {"email": user.email, "id": user.id}
    
    except Exception as e:
        # Manejar cualquier error inesperado
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
