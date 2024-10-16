import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app  # Asegúrate de que "main" sea el nombre correcto de tu archivo principal
from fastapi import HTTPException

client = TestClient(app)

# Test para la ruta raíz "/"
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


    
# Test para las rutas incluidas
@pytest.mark.parametrize("route, status_code", [
    ("/userRegister", 404),  # Actualiza esta ruta según tu configuración
    ("/login", 405),  # Actualiza esta ruta según tu configuración
    ("/createdFund", 404),  # Actualiza esta ruta según tu configuración
    ("/createdAccountMonetary", 404),  # Actualiza esta ruta según tu configuración
    ("/vinculatedBondingFund", 404),  # Actualiza esta ruta según tu configuración
    ("/canceledBodingFund", 405),  # Actualiza esta ruta según tu configuración
    ("/getTransactions", 200),  # Actualiza esta ruta según tu configuración
])
def test_included_routes(route, status_code):
    response = client.get(route)
    assert response.status_code == status_code  # Cambia el código esperado si tus rutas están definidas
