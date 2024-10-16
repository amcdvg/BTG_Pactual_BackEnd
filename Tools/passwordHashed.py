from datetime import datetime
import hashlib

# Función para cifrar la contraseña con SHA-256
def hashPasswordSha256(password: str) -> str:
    shaSignature = hashlib.sha256(password.encode()).hexdigest()
    return shaSignature


result = hashPasswordSha256("miContraseñaSegura")
print(result)