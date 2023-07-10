# IMPORTAR HERRAMIENTAS
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow

# Crear la app
app = Flask(__name__)

# Usar Cors para dar acceso a las rutas(ebdpoint) desde frontend
CORS(app)

# CONFIGURACIÓN A LA BASE DE DATOS DESDE app
#  (SE LE INFORMA A LA APP DONDE UBICAR LA BASE DE DATOS)
                                                    # //username:password@url/nombre de la base de datos
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://ig23033:XXX@ig23033.mysql.pythonanywhere-services.com/ig23033$recetas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# COMUNICAR LA APP CON SQLALCHEMY
db = SQLAlchemy(app)

# PERMITIR LA TRANSFORMACIÓN DE DATOS
ma = Marshmallow(app)


# ESTRUCTURA DE LA TABLA producto A PARTIR DE LA CLASE
class Producto(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    nombrereceta = db.Column(db.String(100))
    linkreceta = db.Column(db.String(100))
    comentarios = db.Column(db.String(100))

    def __init__(self,nombrereceta,linkreceta,comentarios):
        self.nombrereceta = nombrereceta
        self.linkreceta = linkreceta
        self.comentarios = comentarios


# CÓDIGO PARA CREAR LAS TABLAS DEFINIDAS EN LAS CLASES
with app.app_context():
    db.create_all()

# CREAR UNA CLASE  ProductoSchema, DONDE SE DEFINEN LOS CAMPOS DE LA TABLA
class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','nombrereceta','linkreceta','comentarios')


# DIFERENCIAR CUANDO SE TRANSFORME UN DATO O UNA LISTA DE DATOS
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)


# CREAR LAS RUTAS PARA: productos
# '/recetas' ENDPOINT PARA MOSTRAR TODOS LOS PRODUCTOS DISPONIBLES EN LA BASE DE DATOS: GET
# '/recetas' ENDPOINT PARA RECIBIR DATOS: POST
# '/recetas/<id>' ENDPOINT PARA MOSTRAR UN PRODUCTO POR ID: GET
# '/recetas/<id>' ENDPOINT PARA BORRAR UN PRODUCTO POR ID: DELETE
# '/recetas/<id>' ENDPOINT PARA MODIFICAR UN PRODUCTO POR ID: PUT

@app.route("/recetas", methods=['GET'])
def get_productos():
                    # select * from producto
    all_productos = Producto.query.all()
    # Almacena un listado de objetos

    return productos_schema.jsonify(all_productos)


@app.route("/recetas", methods=['POST'])
def create_productos():
    """
    Entrada de datos:
    {
        "nombrereceta": "Pastas XYZ",
        "linkreceta": "https://XYZ.com",
        "comentarios": "La mejor receta!"
}
    """
    nombrereceta = request.json['nombrereceta']
    linkreceta = request.json['linkreceta']
    comentarios = request.json['comentarios']

    new_producto = Producto(nombrereceta, linkreceta, comentarios)
    db.session.add(new_producto)
    db.session.commit()

    return producto_schema.jsonify(new_producto)


@app.route("/recetas/<id>", methods=['GET'])
def get_producto(id):
    producto = Producto.query.get(id)

    return producto_schema.jsonify(producto)


@app.route('/recetas/<id>',methods=['DELETE'])
def delete_producto(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    producto=Producto.query.get(id)

    # A partir de db y la sesión establecida con la base de datos borrar
    # el producto.
    # Se guardan lo cambios con commit
    db.session.delete(producto)
    db.session.commit()

    return producto_schema.jsonify(producto)


@app.route('/recetas/<id>',methods=['PUT'])
def update_producto(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    producto=Producto.query.get(id)

    #  Recibir los datos a modificar
    nombrereceta=request.json['nombrereceta']
    linkreceta=request.json['linkreceta']
    comentarios=request.json['comentarios']

    # Del objeto resultante de la consulta modificar los valores
    producto.nombrereceta=nombrereceta
    producto.linkreceta=linkreceta
    producto.comentarios=comentarios
#  Guardar los cambios
    db.session.commit()
# Para ello, usar el objeto producto_schema para que convierta con                     # jsonify el dato recién eliminado que son objetos a JSON
    return producto_schema.jsonify(producto)

@app.route('/')
def hello_wordl():
	return 'Bienvenido a la aplicación web: Recetas!'
