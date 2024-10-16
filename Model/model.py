from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import List,Optional
from datetime import datetime
from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from hashlib import sha256


# Herramientas para manejar ObjectId en Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid object ID')
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.str_schema()

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler: GetCoreSchemaHandler) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        return {
            **json_schema,
            "type": "string",
            "format": "objectid",
        }
        


# Clase base con la configuración común
class BaseModelConfig(BaseModel):
    class Config:
        #allow_population_by_field_name = True
        populate_by_name = True
        json_encoders = {ObjectId: str}


# Modelo de vinculación de Fondos
class BondingFund(BaseModelConfig):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    fundId: PyObjectId = Field(default_factory=PyObjectId)
    investedAmount: int
    bondingDate: datetime
    userId: PyObjectId = Field(default_factory=PyObjectId)
    notificationPreferences: str
    notificationId: PyObjectId = Field(default_factory=PyObjectId)
    uniqueNumber: str

# Modelo de la colección "Notificaciones"
class Notification(BaseModelConfig):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    transactionId: PyObjectId = Field(default_factory=PyObjectId)
    medium: str  # "email" o "sms"
    sendDate: datetime


# Modelo de la colección "Fondos"
class Fund(BaseModelConfig):
    id: PyObjectId = Field(default_factory=PyObjectId)
    name: str
    minimumAmount: int
    category: str


# Modelo de la colección "Transacciones"
class Transaction(BaseModelConfig):
    id: PyObjectId = Field(default_factory=PyObjectId)
    bondingFundId: PyObjectId = Field(default_factory=PyObjectId)
    fundId: PyObjectId = Field(default_factory=PyObjectId)
    type: str  # "apertura" o "cancelacion"
    amount: int
    date: datetime
    status: str  # "completado" o "error"
    uniqueNumber: str
    


# Modelo de la colección "Usuarios"
class User(BaseModelConfig):
    id: PyObjectId = Field(default_factory=PyObjectId) #PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    hashedPassword: str
    fullName: str
    phoneNumber: str
    isActive: bool
    isSuperuser: bool
    createdAt: datetime
    

# Modelo de la colección "AccountMonetary"
class AccountMonetary(BaseModelConfig):
    id: PyObjectId = Field(default_factory=PyObjectId) #PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userId: PyObjectId = Field(default_factory=PyObjectId)
    amount: int
    createdAt: datetime
