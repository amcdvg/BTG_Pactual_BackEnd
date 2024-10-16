from fastapi import FastAPI, HTTPException, Depends, APIRouter
from pydantic import BaseModel
import jwt
import datetime
from passlib.context import CryptContext
import boto3
from boto3.dynamodb.conditions import Key
from Tools.passwordHashed import hashPasswordSha256
from Data.data import connection
from Model.model import User
import os
from dotenv import load_dotenv
from rapidfuzz import fuzz
from fastapi.responses import JSONResponse

appLogin = APIRouter()

# Configuración de contraseñas y JWT
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Acceder a la tabla Users de DynamoDB
usersTable = connection("Users")
tokensTable = connection('InvalidTokens')  # Tabla para almacenar tokens invalidados

# Función para crear un token
def createAccessToken(email: str):
    # Cargar las variables del archivo .env
    load_dotenv()
    # Acceder a las variables del .env para la conexión de la base de datos
    secretKey = os.getenv("SECRETKEY")
    algorithmSha = os.getenv("ALGORITHM")
    # Crear Token
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token válido por 1 hora
    token = jwt.encode({"sub": email, "exp": expire}, secretKey, algorithm=algorithmSha)
    return token

# Endpoint de login
@appLogin.post("/login/")
async def loginUser(email: str, password: str):
    # Buscar el usuario en DynamoDB
    response = usersTable.query(
            IndexName='EmailIndex',  # Nombre del índice secundario
            KeyConditionExpression=Key('email').eq(email)
        )
    # Obtener usuarios y contraseñas encriptadas
    user = response.get('Items')
    print(response)
    print(password)
    userConsult = user[0]
    shaPassWord = hashPasswordSha256(password)
    #Validación si el usuario existe o la contraseña es la correcta
    if not user or not fuzz.ratio(shaPassWord, userConsult["hashedPassword"]) == 100.0:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    # Creación de
    token = createAccessToken(email=email)
    return JSONResponse(
                status_code=200,
                content={
                    "status": 200,
                    "message": "Operation was successful",
                    "data":  {"message": "Login successful", "token": token, "nameUser":userConsult["fullName"]}
                }
            )
    return

# Endpoint de logout
@appLogin.post("/logout/")
async def logoutUser(token: str):
    # Agregar el token a la tabla de tokens invalidados
    #tokensTable.put_item(Item={"token": token})
    return {"message": "Logout successful"}


