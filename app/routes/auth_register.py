# routes/auth_register.py
from fastapi import APIRouter, HTTPException
from app.models.user import UsuarioRegistro
from app.db.conexion_mongo import get_db
from datetime import datetime
from passlib.hash import bcrypt

router = APIRouter(prefix="/auth", tags=["Registro"])

@router.post("/register")
async def registrar_usuario(datos: UsuarioRegistro):
    db, client = get_db()
    usuarios = db["Usuarios"]

    # Verifica si ya existe un usuario con el mismo correo
    if usuarios.find_one({"correo": datos.correo}):
        client.close()
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

    # Crear documento de usuario
    nuevo_usuario = {
        "nombre": datos.nombre,
        "correo": datos.correo,
        "password_hash": bcrypt.hash(datos.password),  # Contraseña encriptada
        "proveedor": "local",
        "rol": "usuario",
        "fecha_registro": datetime.utcnow(),
        "foto": None
    }

    usuarios.insert_one(nuevo_usuario)
    client.close()

    return {"status": "ok", "mensaje": "Usuario registrado exitosamente"}