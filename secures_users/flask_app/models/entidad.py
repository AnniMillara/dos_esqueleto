from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

DB = "esqueleto"


class Entidades:
    def __init__(self, data):
        self.id_entidad = data["id_entidad"]
        self.titulo = data["titulo"]
        self.descripcion = data["descripcion"]
        self.usuario_id = data["usuario_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.autor_nombre = data.get("autor_nombre")
        self.autor_apellido = data.get("autor_apellido")

    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO entidades (
                titulo, 
                descripcion, 
                usuario_id, 
                created_at, 
                updated_at
            ) VALUES (
                %(titulo)s, 
                %(descripcion)s, 
                %(usuario_id)s, 
                NOW(), 
                NOW()
            );
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def ver_todas(cls):
        query = """
            SELECT 
                e.id_entidad,
                e.titulo,
                e.descripcion,
                e.usuario_id,
                e.created_at,
                e.updated_at,
                u.nombre AS autor_nombre,
                u.apellido AS autor_apellido
            FROM entidades e
            JOIN usuarios u ON e.usuario_id = u.id_usuario
            ORDER BY e.id_entidad;
        """
        resultados = connectToMySQL(DB).query_db(query)
        entidades = []
        for entidad in resultados:
            entidades.append(cls(entidad))
        return entidades

    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                e.id_entidad,
                e.titulo,
                e.descripcion,
                e.usuario_id,
                e.created_at,
                e.updated_at,
                u.nombre AS autor_nombre,
                u.apellido AS autor_apellido
            FROM entidades e
            JOIN usuarios u ON e.usuario_id = u.id_usuario
            WHERE e.id_entidad = %(id_entidad)s;
        """
        data = {"id_entidad": id}
        resultado = connectToMySQL(DB).query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @classmethod
    def modificar(cls, data):
        query = """
            UPDATE entidades
            SET 
                titulo = %(titulo)s,
                descripcion = %(descripcion)s,
                updated_at = NOW()
            WHERE id_entidad = %(id_entidad)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM entidades
            WHERE id_entidad = %(id_entidad)s;
        """
        data = {"id_entidad": id}
        return connectToMySQL(DB).query_db(query, data)

    @staticmethod
    def validar(datos):
        es_valido = True

        if not datos["titulo"].strip():
            flash("El título es obligatorio.", "error"); es_valido = False
        elif len(datos["titulo"].strip()) < 2:
            flash("El título debe tener al menos 2 caracteres.", "error"); es_valido = False

        if not datos["descripcion"].strip():
            flash("La descripción es obligatoria.", "error"); es_valido = False
        elif len(datos["descripcion"].strip()) < 10:
            flash("La descripción debe tener al menos 10 caracteres.", "error"); es_valido = False

        return es_valido