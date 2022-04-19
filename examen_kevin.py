# KEVIN AXELL BARRA MORALES
# SEGUNDO EXAMEN
# ARQUITECTURA DE SOFtWARE

from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mibdusuarios.db"

db = SQLAlchemy(app)

ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    papellido = db.Column(db.String(255))
    mapellido = db.Column(db.String(255))
    correo_elect = db.Column(db.String(255))
    nombre_usuario = db.Column(db.String(255))
    ultimo_acceso = db.Column(db.String(255))
    departamento = db.Column(db.String(255))
    turno = db.Column(db.String(255))
    RFFID = db.Column(db.Integer)
    personal_externo = db.Column(db.Boolean)
    RRHH = db.Column(db.Boolean)

    def __init__(self, nombre, papellido, mapellido, correo_elect, nombre_usuario, ultimo_acceso, departamento, turno, RFFID, personal_externo, RRHH):
        self.nombre = nombre
        self.papellido = papellido
        self.mapellido = mapellido
        self.correo_elect = correo_elect
        self.nombre_usuario = nombre_usuario
        self.ultimo_acceso = ultimo_acceso
        self.departamento = departamento
        self.turno = turno
        self.RFFID = RFFID
        self.personal_externo = personal_externo
        self.RRHH = RRHH


# Crea la base de datos se comenta despues
db.create_all()


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "nombre", "papellido", "mapellido", "correo_elect", "nombre_usuario", "ultimo_acceso", "departamento", "turno", "RFFID", "personal_externo", "RRHH")


userSchema = UserSchema()

userSchema = UserSchema(many=True)

users = [{}]

usuarios = User.query.all()
print(usuarios)


@app.route("/")
def hello_world():
    return "Hola Mundo"


@app.route("/api/usuarios/", methods=["GET"])
def get_users():
    return jsonify({"users": usuarios})


@app.route("/api/usuarios/" + "<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({"user": user})


@app.route("/api/usuarios/", methods=["POST"])
def create_user():
    if not request.json:
        abort(404)
    new_user = User(nombre=request.json["nombre"], papellido=request.json["papellido"], mapellido=request.json["mapellido"], correo_elect=request.json["correo_elect"], nombre_usuario=request.json["nombre_usuario"], ultimo_acceso=datetime.datetime.now(), departamento=request.json["departamento"], turno=request.json["turno"], RFFID=request.json["RFFID"], personal_externo=request.json["personal_externo"], RRHH=request.json["RRHH"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"user": new_user}), 201


@app.route("/api/usuarios/" + "<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if not request.json:
        abort(400)

    user = User.query.get_or_404(user_id)

    user.nombre = request.json["nombre"]
    db.session.commit()

    user.papellido = request.json["papellido"]
    db.session.commit()

    user.mapellido = request.json["mapellido"]
    db.session.commit()

    user.correo_elect = request.json["correo_elect"]
    db.session.commit()

    user.nombre_usuario = request.json["nombre_usuario"]
    db.session.commit()

    user.ultimo_acceso = datetime.datetime.now()
    db.session.commit()

    user.departamento = request.json["departamento"]
    db.session.commit()

    user.RFFID = request.json["RFFID"]
    db.session.commit()

    user.turno = request.json["turno"]
    db.session.commit()

    user.personal_externo = request.json["personal_externo"]
    db.session.commit()

    user.RRHH = request.json["RRHH"]
    db.session.commit()

    return jsonify({"user": User.as_dict(user)}), 201


@app.route("/api/usuarios/" + "<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"result": True})


if __name__ == "__main__":
    app.run(debug=True)
