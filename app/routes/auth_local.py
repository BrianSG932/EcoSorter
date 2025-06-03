# app/routes/auth_local.py

from fastapi import APIRouter, HTTPException
from app.models.user import UsuarioLogin
from app.db.conexion_mongo import get_db
from passlib.hash import bcrypt

router = APIRouter(prefix="/auth", tags=["Autenticación local"])

@router.post("/login")
async def login_usuario(datos: UsuarioLogin):
    db, client = get_db()
    usuarios = db["Usuarios"]

    usuario = usuarios.find_one({"correo": datos.correo, "proveedor": "local"})

    if not usuario:
        client.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not usuario.get("password_hash") or not bcrypt.verify(datos.password, usuario["password_hash"]):
        client.close()
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    client.close()
    return {
        "status": "ok",
        "usuario": {
            "nombre": usuario["nombre"],
            "correo": usuario["correo"],
            "rol": usuario["rol"],
            "foto": usuario.get("foto", "")
        }
    }