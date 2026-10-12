from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "clave_secreta_esqueleto"
bcrypt = Bcrypt(app)

from flask_app.controllers import usuarios, entidades