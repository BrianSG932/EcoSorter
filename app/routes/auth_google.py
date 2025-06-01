# auth_google.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
from app.db.conexion_mongo import get_db
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class TokenPayload(BaseModel):
    token_id: str

GOOGLE_CLIENT_ID = "718055390256-qqtfi2l9usdq4r4v10efj6q0didi3svr.apps.googleusercontent.com"  # Desde consola Google

@router.post("/google-login")
async def login_con_google(payload: TokenPayload):
    try:
        # Verificar token con Google
        idinfo = id_token.verify_oauth2_token(payload.token_id, requests.Request(), GOOGLE_CLIENT_ID)

        # idinfo contiene info del usuario
        user_email = idinfo['email']
        user_name = idinfo.get('name', 'NoName')
        picture = idinfo.get('picture', '')
        proveedor = "google"

        db, client = get_db()
        usuarios = db["Usuarios"]

        # Buscar usuario
        usuario = usuarios.find_one({"correo": user_email})

        # Si no existe, lo crea
        if not usuario:
            nuevo_usuario = {
                "nombre": user_name,
                "correo": user_email,
                "foto": picture,
                "proveedor": proveedor,
                "rol": "usuario",
                "fecha_registro": datetime.utcnow(),
                "password_hash": None
            }
            usuarios.insert_one(nuevo_usuario)
            usuario = nuevo_usuario

        client.close()

        # Aquí podrías validar si el usuario ya existe en MongoDB, y si no, crearlo
        return {
            "status": "ok",
            "user": {
                "nombre": usuario["nombre"],
                "correo": usuario["correo"],
                "foto": usuario.get("foto", ""),
                "rol": usuario.get("rol", "usuario")
            }
        }

    except ValueError as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")