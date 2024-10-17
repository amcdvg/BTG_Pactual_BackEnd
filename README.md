
# Prueba Tecnica - btg Pactal - seti - BackEnd

## FastAPI

El presente proyecto es una prueba tecnica. Paara el desarrollo del BackEnd se uso el lenguaje de programación Python versión 3.10. Por tanto, para desarrollar la aplicación wen con  API REST se usó el framework FastAPI, permitiendo al usuario disponer de la funcionalidad descrita:

Por tanto el proyecto tiene la sigiente arquitectura:


```bash
  Data
     data.py 
  Config
     config.py
  Model
     Model.py
  Router
     cancelBodingFund.py
     ...
  Tools
     convertDecimalFloat.py
     ...
  Utils
     senEmail
        sendEmail.py
     senMSM
        sendMsm.py
  test
     ...
  main.py
  requirements.txt

```

Por lo tanto podemos identificar que en FastAPI, tiene los siguientes patrones de diseño

### Factory Method en FastAPI

El Factory Method permite crear instancias de objetos según el tipo de dependencia requerida. En FastAPI, podrías utilizar este patrón para generar servicios o controladores específicos basados en la configuración o tipo de solicitud.

```bash
from fastapi import FastAPI, Depends

app = FastAPI()

# Definimos una fábrica que crea servicios específicos basados en algún criterio
class ServiceBase:
    def serve(self):
        raise NotImplementedError

class EmailService(ServiceBase):
    def serve(self):
        return "Sending an email"

class SMSService(ServiceBase):
    def serve(self):
        return "Sending an SMS"

def service_factory(service_type: str) -> ServiceBase:
    if service_type == "email":
        return EmailService()
    elif service_type == "sms":
        return SMSService()
    else:
        raise ValueError("Unsupported service type")

# Usamos el Factory Method para inyectar el servicio adecuado en el endpoint
@app.get("/notify/")
def notify(service: ServiceBase = Depends(service_factory("email"))):
    return {"message": service.serve()}

```

### Builder en FastAPI
El patrón Builder es útil cuando deseas construir objetos o configuraciones complejas de manera escalonada. En FastAPI, podrías usar este patrón para crear una configuración avanzada de una aplicación o de un servicio.

```bash
from fastapi import FastAPI

# Definimos un Builder para configurar la aplicación
class AppBuilder:
    def __init__(self):
        self._app = FastAPI()

    def set_router(self, router):
        self._app.include_router(router)
        return self

    def add_middleware(self, middleware):
        self._app.add_middleware(middleware)
        return self

    def build(self):
        return self._app

# Un ejemplo de router para incluir
from fastapi import APIRouter
router = APIRouter()

@router.get("/items/")
def read_items():
    return [{"item": "item1"}, {"item": "item2"}]

# Construcción de la aplicación usando el Builder
app_builder = AppBuilder()
app = app_builder.set_router(router).build()

# FastAPI correrá la app con las configuraciones que hemos agregado

```

### Singleton en FastAPI

El patrón Singleton garantiza que una clase tenga solo una instancia y proporcione un punto de acceso global a ella. En FastAPI, podrías usar este patrón para servicios que solo deberían tener una única instancia, como un cliente de base de datos.

```bash
from fastapi import FastAPI, Depends

app = FastAPI()

# Implementación del patrón Singleton para una clase de base de datos
class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = "Database Connection"
        return cls._instance

    def get_connection(self):
        return self.connection

# Creando una dependencia que siempre devuelva la misma instancia de Database
def get_database() -> Database:
    return Database()

@app.get("/db/")
def get_db_connection(db: Database = Depends(get_database)):
    return {"db_connection": db.get_connection()}


```

## Instalación
Para correr localmente puedes usar los siguientes comandos

```bash
pip install -r requirements.txt

```

## Ejecutar localmente 
Puedes ejecutar localmente este proyecto con el siguiente comandos

```bash
uvicorn main:app --reload

```

## Servicio desplegado en AWS

```bash
http://98.82.200.42:8000/docs

```

para el despliegue se realizó en una instancia EC2 en el que se utulizó un la herrmaienta

```bash
pm2 start "uvicorn main:app --host 0.0.0.0 --reload

```

