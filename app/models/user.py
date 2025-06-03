from pydantic import BaseModel

class UsuarioRegistro(BaseModel):
    nombre: str
    correo: str
    password: str

class UsuarioLogin(BaseModel):
    correo: str
    password: str