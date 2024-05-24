from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Gestión de Empleados API',
          description='API para administrar áreas y empleados')

# Definición del modelo de área
area_model = api.model('Área', {
    'id': fields.Integer(required=True, description='ID del área'),
    'nombre': fields.String(required=True, description='Nombre del área'),
    'piso': fields.Integer(required=True, description='Piso del área')
})

# Definición del modelo de empleado
empleado_model = api.model('Empleado', {
    'id': fields.Integer(required=True, description='ID del empleado'),
    'nombre': fields.String(required=True, description='Nombre del empleado'),
    'apellido': fields.String(required=True, description='Apellido del empleado'),
    'email': fields.String(required=True, description='Email del empleado'),
    'area_id': fields.Integer(required=True, description='ID del área al que pertenece el empleado')
})

# Datos de ejemplo para áreas y empleados
areas = [
    {"id": 1, "nombre": "Marketing", "piso": 1},
    {"id": 2, "nombre": "Sistemas", "piso": 2},
    {"id": 3, "nombre": "Contabilidad", "piso": 3}
]

empleados = [
    {"id": 1, "nombre": "Juan", "apellido": "Perez", "email": "juan@example.com", "area_id": 1},
    {"id": 2, "nombre": "Maria", "apellido": "Gomez", "email": "maria@example.com", "area_id": 2},
    {"id": 3, "nombre": "Pedro", "apellido": "Lopez", "email": "pedro@example.com", "area_id": 1}
]


@api.route('/areas')
class AreaList(Resource):
    @api.doc('Lista de todas las áreas')
    def get(self):
        return areas

    @api.doc('Crear un nueva área')
    @api.expect(area_model)
    def post(self):
        nueva_area = api.payload
        areas.append(nueva_area)
        return nueva_area, 201


@api.route('/area/<int:id>')
class AreaDetail(Resource):
    @api.doc('Obtener detalles de un área por ID')
    def get(self, id):
        for area in areas:
            if area['id'] == id:
                return area
        return {'mensaje': 'Área no encontrada'}, 404


@api.route('/empleados')
class EmpleadoList(Resource):
    @api.doc('Lista de todos los empleados')
    def get(self):
        return empleados

    @api.doc('Crear un nuevo empleado')
    @api.expect(empleado_model)
    def post(self):
        nuevo_empleado = api.payload
        empleados.append(nuevo_empleado)
        return nuevo_empleado, 201


@api.route('/empleados/filtrar')
@api.doc(params={'email': 'Filtrar por email', 'nombre': 'Filtrar por nombre'})
class EmpleadoFilter(Resource):
    @api.doc('Filtrar empleados por email o nombre')
    def get(self):
        email = request.args.get('email')
        nombre = request.args.get('nombre')

        if email:
            empleados_filtrados = [empleado for empleado in empleados if empleado['email'] == email]
        elif nombre:
            empleados_filtrados = [empleado for empleado in empleados if empleado['nombre'] == nombre]
        else:
            empleados_filtrados = empleados

        return empleados_filtrados


if __name__ == '__main__':
    app.run(debug=True)
