import pytest
from pydantic_settings import BaseSettings
from Config.config import config  # Asegúrate de importar tu clase correctamente

def test_config_defaults():
    settings = config()
    assert settings.containerName == 'BTG Pactual'
    assert settings.version == '0.0.1'
    assert settings.projectName == 'BackEnd BTG Pactual'
    assert settings.description == 'Resful API -  Prueba Técnica para Ingeniero de Desarrollo Fullstack'

def test_config_env_variables(monkeypatch):
    # Usar monkeypatch para establecer variables de entorno
    monkeypatch.setenv('CONTAINERNAME', 'New Container')
    monkeypatch.setenv('VERSION', '1.0.0')
    monkeypatch.setenv('PROJECTNAME', 'New Project')
    monkeypatch.setenv('DESCRIPTION', 'New Description')

    settings = config()
    assert settings.containerName == 'New Container'
    assert settings.version == '1.0.0'
    assert settings.projectName == 'New Project'
    assert settings.description == 'New Description'
