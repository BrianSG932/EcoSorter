from pydantic import BaseModel

class UsuarioRegistro(BaseModel):
    nombre: str
    correo: str
    password: str