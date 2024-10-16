from fastapi import FastAPI
from Config.config import settings
from Router.userRegister import appUserRegister
from Router.login import appLogin, tokensTable
from Router.createdFund import appFunds
from Router.createdAccountMonetary import appAccountMonetary
from Router.vinculatedBondingFund import appFundInvesting
from Router.cancelBodingFund import appCancelFundInvesting
from Router.getTransactions import appgetTransationbtg
from Router.getFundViculate import appgetFundViculate
from fastapi.middleware.cors import CORSMiddleware
# application.include_router(api_router)

def getApplication() -> FastAPI:
    tagsMetadata = [
        {
            'name' : 'BTG Pactual',
            'description': 'Prueba Técnica para Ingeniero de Desarrollo Fullstack',
        }
    ]
    
    application = FastAPI(
        title = settings.projectName,
        version = settings.version,
        description = settings.description,
        openapiTags = tagsMetadata
    )
    application.include_router(appUserRegister)
    application.include_router(appLogin)
    application.include_router(appFunds)
    application.include_router(appAccountMonetary)
    application.include_router(appFundInvesting)
    application.include_router(appCancelFundInvesting)
    application.include_router(appgetTransationbtg)
    application.include_router(appgetFundViculate)
    
    origins = [
        '*',
    ]
    
    application.add_middleware(
        CORSMiddleware,
        allow_origins = origins,
        allow_credentials = True,
        allow_methods = ['*'],
        allow_headers = ['*'],
    )
    
    return application



app = getApplication()
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Middleware para verificar tokens
@app.middleware("http")
async def verifyToken(request, call_next):
    token = request.headers.get("Authorization")
    if token:
        token = token.split(" ")[1]  # Asumiendo formato "Bearer <token>"
        # Verificar si el token está en la tabla de tokens invalidados
        response = tokensTable.get_item(Key={"token": token})
        if 'Item' in response:
            raise HTTPException(status_code=401, detail="Token has been invalidated")
        
    response = await call_next(request)
    return response