from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuarios


@app.route("/")
def inicio():
    if "id_usuario" in session:
        return redirect(url_for("listado_entidades"))
    return render_template("login.html")


@app.route("/registro", methods=["POST"])
def registro():
    datos = {
        "nombre": request.form.get("nombre", "").strip(),
        "apellido": request.form.get("apellido", "").strip(),
        "email": request.form.get("email", "").strip(),
        "contrasena": request.form.get("contrasena", "").strip(),
        "confirmar_contrasena": request.form.get("confirmar_contrasena", "").strip(),
    }
    if not Usuarios.validar_registro(datos):
        return redirect(url_for("inicio"))

    hash_pw = bcrypt.generate_password_hash(datos["contrasena"]).decode("utf-8")

    data = {
        "nombre": datos["nombre"],
        "apellido": datos["apellido"],
        "email": datos["email"],
        "contrasena": hash_pw,
    }
    nuevo_id = Usuarios.guardar(data)
    if not nuevo_id:
        flash("No fue posible crear el usuario.", "error")
        return redirect(url_for("inicio"))

    session["id_usuario"] = nuevo_id
    session["nombre"] = datos["nombre"]
    flash("Usuario creado correctamente.", "success")
    return redirect(url_for("listado_entidades"))


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()
    contrasena = request.form.get("contrasena", "").strip()

    if not email or not contrasena:
        flash("Email y contraseña son obligatorios.", "error")
        return redirect(url_for("inicio"))

    usuario = Usuarios.buscar_email(email)
    if not usuario or not bcrypt.check_password_hash(usuario.contrasena, contrasena):
        flash("Email o contraseña incorrectos.", "error")
        return redirect(url_for("inicio"))

    session["id_usuario"] = usuario.id_usuario
    session["nombre"] = usuario.nombre
    flash("Bienvenido de vuelta.", "success")
    return redirect(url_for("listado_entidades"))


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "success")
    return redirect(url_for("inicio"))


@app.route("/perfil")
def perfil():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "error")
        return redirect(url_for("inicio"))

    usuario = Usuarios.buscar_id(session["id_usuario"])
    if not usuario:
        session.clear()
        return redirect(url_for("inicio"))

    return render_template("perfil.html", usuario=usuario)


@app.route("/perfil/eliminar")
def eliminar_usuario():
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))

    Usuarios.eliminar(session["id_usuario"])
    session.clear()
    flash("Perfil eliminado.", "success")
    return redirect(url_for("inicio"))