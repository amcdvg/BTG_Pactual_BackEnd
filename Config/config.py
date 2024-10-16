from pydantic_settings import BaseSettings


class config(BaseSettings):
    containerName: str = 'BTG Pactual'
    version:  str = '0.0.1'
    projectName: str = 'BackEnd BTG Pactual'
    description: str = 'Resful API -  Prueba Técnica para Ingeniero de Desarrollo Fullstack'
    
settings = config()