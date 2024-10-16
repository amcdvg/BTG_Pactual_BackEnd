import pytest
from Tools.passwordHashed import hashPasswordSha256

# Prueba para la función hashPasswordSha256
def test_hashPasswordSha256():
    # Contraseña de ejemplo
    password = "miContraseñaSegura"
    
    # Valor hash esperado (calculado previamente)
    expected_hash = "9581cc6ccd7d9f00794ae3c54d51ee206ed44a7403d18948f4e5a4bf684ce279"  # Este hash se puede calcular en Python antes de ejecutar la prueba
    
    # Llamar a la función y verificar el resultado
    assert hashPasswordSha256(password) == expected_hash

def test_hashPasswordSha256_empty_password():
    # Probar con una contraseña vacía
    password = ""
    expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"  # Hash de una cadena vacía
    
    assert hashPasswordSha256(password) == expected_hash

def test_hashPasswordSha256_special_characters():
    # Probar con una contraseña que tenga caracteres especiales
    password = "P@ssw0rd!"
    expected_hash = "0e44ce7308af2b3de5232e4616403ce7d49ba2aec83f79c196409556422a4927"  # Hash de "P@ssw0rd!"
    
    assert hashPasswordSha256(password) == expected_hash
