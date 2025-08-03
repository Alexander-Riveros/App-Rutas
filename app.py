from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Inicializa Firebase Admin con tu archivo de credenciales (asegúrate que exista)
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://console.firebase.google.com/u/0/project/app-rutas-seguras/database/app-rutas-seguras-default-rtdb/data/~2F?hl=es-419'
})

# Referencia al nodo 'usuarios' en Firebase
usuarios_ref = db.reference('/usuarios')

# Rutas para renderizar todas tus páginas HTML
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/gps')
def gps():
    return render_template('gps.html')

@app.route('/camara')
def camara():
    return render_template('camara.html')

# API REST para gestionar usuarios con Firebase
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    new = usuarios_ref.push(data)
    return jsonify({'id': new.key}), 200

@app.route('/leer_usuarios', methods=['GET'])
def leer_usuarios():
    return jsonify(usuarios_ref.get() or {}), 200

@app.route('/eliminar_usuario/<id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuarios_ref.child(id).delete()
    return jsonify({'mensaje': 'Usuario eliminado'}), 200

if __name__ == '__main__':
    app.run(debug=True)
