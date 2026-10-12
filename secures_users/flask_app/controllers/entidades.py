from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.entidad import Entidades


@app.route("/entidades")
def listado_entidades():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "error")
        return redirect(url_for("inicio"))
    entidades = Entidades.ver_todas()
    return render_template("entidad_lista.html", entidades=entidades)


@app.route("/entidades/nueva")
def nueva_entidad():
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))
    return render_template("entidad_form.html", entidad=None)


@app.route("/entidades/crear", methods=["POST"])
def crear_entidad():
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))

    datos = {
        "titulo": request.form.get("titulo", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "usuario_id": session["id_usuario"],
    }
    if not Entidades.validar(datos):
        return redirect(url_for("nueva_entidad"))

    Entidades.guardar(datos)
    flash("Registro guardado correctamente.", "success")
    return redirect(url_for("listado_entidades"))


@app.route("/entidades/detalle/<int:id>")
def detalle_entidad(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))

    entidad = Entidades.buscar_id(id)
    if not entidad:
        flash("No encontrado.", "error")
        return redirect(url_for("listado_entidades"))
    return render_template("entidad_detalle.html", entidad=entidad)


@app.route("/entidades/editar/<int:id>")
def editar_entidad(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))

    entidad = Entidades.buscar_id(id)
    if not entidad:
        return redirect(url_for("listado_entidades"))
    if entidad.usuario_id != session["id_usuario"]:
        flash("No puedes editar este registro.", "error")
        return redirect(url_for("listado_entidades"))

    return render_template("entidad_form.html", entidad=entidad)


@app.route("/entidades/modificar/<int:id>", methods=["POST"])
def modificar_entidad(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))

    entidad = Entidades.buscar_id(id)
    if not entidad or entidad.usuario_id != session["id_usuario"]:
        flash("No puedes modificar este registro.", "error")
        return redirect(url_for("listado_entidades"))

    datos = {
        "id_entidad": id,
        "titulo": request.form.get("titulo", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
    }
    if not Entidades.validar(datos):
        return redirect(url_for("editar_entidad", id=id))

    Entidades.modificar(datos)
    flash("Registro actualizado correctamente.", "success")
    return redirect(url_for("listado_entidades"))


@app.route("/entidades/confirmar_eliminar/<int:id>")
def confirmar_eliminar_entidad(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))

    entidad = Entidades.buscar_id(id)
    if not entidad or entidad.usuario_id != session["id_usuario"]:
        return redirect(url_for("listado_entidades"))

    return render_template(
        "confirmar_eliminar.html",
        mensaje=f"Vas a eliminar '{entidad.titulo}'. Esta acción no se puede deshacer.",
        accion=url_for("eliminar_entidad", id=id),
        cancelar=url_for("listado_entidades")
    )


@app.route("/entidades/eliminar/<int:id>")
def eliminar_entidad(id):
    if "id_usuario" not in session:
        return redirect(url_for("inicio"))

    entidad = Entidades.buscar_id(id)
    if not entidad or entidad.usuario_id != session["id_usuario"]:
        flash("No puedes eliminar este registro.", "error")
        return redirect(url_for("listado_entidades"))

    Entidades.eliminar(id)
    flash("Registro eliminado.", "success")
    return redirect(url_for("listado_entidades"))