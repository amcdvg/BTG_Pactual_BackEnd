from fastapi import FastAPI, HTTPException, Depends
from bson import ObjectId
from Data.data import conection, PyMongoError


app = FastAPI()

# Endpoint para crear un nuevo cliente
@app.post("/clients/")
async def create_cliente(client: Client):
    try:
        collection = conection("client") 
        dataClient = client.dict(by_alias=True)
        result = await collection.insert_one(dataClient)
        return {"id": str(result.inserted_id)}
    except PyMongoError as e:
        # Si ocurre un error relacionado con MongoDB
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        # Cualquier otro error inesperado
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Endpoint para crear un nuevo fondo
@app.post("/funds/")
async def create_fondo(fund: Fund):
    try:
        collection = conection("funds") 
        dataFund = fund.dict(by_alias=True)
        result = await collection.insert_one(dataFund)
        return {"id": str(result.inserted_id)}
    except PyMongoError as e:
        # Si ocurre un error relacionado con MongoDB
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        # Cualquier otro error inesperado
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


# Endpoint para obtener un cliente por ID
@app.get("/clients/{cliente_id}", response_model=Client)
async def get_cliente(clientId: str):
    try:
        collection = conection("client") 
        client = await collection.find_one({"_id": ObjectId(clientId)})
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")
        return client
    except PyMongoError as e:
        # Si ocurre un error relacionado con MongoDB
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        # Cualquier otro error inesperado
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Endpoint para crear una nueva transacción
@app.post("/transaccions/")
async def create_transaccion(transaction: Transaction):
    try:
        collection = conection("transaction") 
        dataTransaction = transaction.dict(by_alias=True)
        result = await collection.insert_one(dataTransaction)
        return {"id": str(result.inserted_id)}
    except PyMongoError as e:
        # Si ocurre un error relacionado con MongoDB
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        # Cualquier otro error inesperado
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

