import smtplib
import re
from email.message import EmailMessage
import os

clave_app = os.environ.get("CLAVE_APP")
remitente = os.environ.get("CORREO_REMITENTE")

def enviar_correo(destinatario, remitente, clave_app):
    mensaje = EmailMessage()
    mensaje["Subject"] = "Registro exitoso en la app de taxis"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje.set_content(
        f"""Hola,

Tu registro en la app de taxis fue exitoso.
Ya puedes iniciar sesión y comenzar a usar el sistema.

¡Bienvenido!"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remitente, clave_app)
        smtp.send_message(mensaje)

def es_correo_valido(correo):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, correo)

def dominio_permitido(correo):
    dominios_validos = ["gmail.com", "uaemex.mx", "outlook.com"]
    dominio = correo.split("@")[-1].lower()
    return dominio in dominios_validos

def correo_autorizado(correo):
    return es_correo_valido(correo) and dominio_permitido(correo)