import re
import bcrypt
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

DB = "esqueleto"


class Usuarios:
    def __init__(self, data):
        self.id_usuario = data["id_usuario"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.contrasena = data["contrasena"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO usuarios (
                nombre, 
                apellido, 
                email, 
                contrasena, 
                created_at, 
                updated_at
            ) VALUES (
                %(nombre)s, 
                %(apellido)s, 
                %(email)s, 
                %(contrasena)s, 
                NOW(), 
                NOW()
            );
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                id_usuario,
                nombre,
                apellido,
                email,
                contrasena,
                created_at,
                updated_at
            FROM usuarios
            WHERE id_usuario = %(id_usuario)s;
        """
        data = {"id_usuario": id}
        resultado = connectToMySQL(DB).query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @classmethod
    def buscar_email(cls, email):
        query = """
            SELECT 
                id_usuario,
                nombre,
                apellido,
                email,
                contrasena,
                created_at,
                updated_at
            FROM usuarios
            WHERE email = %(email)s;
        """
        data = {"email": email}
        resultado = connectToMySQL(DB).query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @classmethod
    def modificar(cls, data):
        query = """
            UPDATE usuarios
            SET 
                nombre = %(nombre)s,
                apellido = %(apellido)s,
                email = %(email)s,
                updated_at = NOW()
            WHERE id_usuario = %(id_usuario)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM usuarios
            WHERE id_usuario = %(id_usuario)s;
        """
        data = {"id_usuario": id}
        return connectToMySQL(DB).query_db(query, data)

    @staticmethod
    def validar_registro(datos):
        es_valido = True

        if not datos["nombre"].strip():
            flash("El nombre es obligatorio.", "error"); es_valido = False
        elif len(datos["nombre"].strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "error"); es_valido = False

        if not datos["apellido"].strip():
            flash("El apellido es obligatorio.", "error"); es_valido = False
        elif len(datos["apellido"].strip()) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "error"); es_valido = False

        if not datos["email"].strip():
            flash("El email es obligatorio.", "error"); es_valido = False
        elif not EMAIL_REGEX.match(datos["email"].strip()):
            flash("El email no tiene un formato válido.", "error"); es_valido = False
        elif Usuarios.buscar_email(datos["email"].strip()):
            flash("El email ya está registrado.", "error"); es_valido = False

        if not datos["contrasena"]:
            flash("La contraseña es obligatoria.", "error"); es_valido = False
        elif len(datos["contrasena"]) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error"); es_valido = False

        if datos.get("confirmar_contrasena") is not None:
            if datos["contrasena"] != datos["confirmar_contrasena"]:
                flash("Las contraseñas no coinciden.", "error"); es_valido = False

        return es_valido