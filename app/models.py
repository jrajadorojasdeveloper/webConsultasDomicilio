from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.Text, nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    cp = db.Column(db.String(10), nullable=False)
    mascota_tipo = db.Column(db.String(50), nullable=False)
    mascota_edad = db.Column(db.String(50))
    motivo = db.Column(db.Text, nullable=False)
    zona = db.Column(db.String(100), nullable=False)
    fecha_pref = db.Column(db.Date, nullable=False)
    hora_pref = db.Column(db.Time, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, confirmada, completada, cancelada
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    nota_interna = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Cita {self.nombre} - {self.fecha_pref}>'

class MensajeContacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    asunto = db.Column(db.String(200), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MensajeContacto {self.nombre} - {self.asunto}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    extracto = db.Column(db.Text)
    contenido = db.Column(db.Text, nullable=False)
    fecha_pub = db.Column(db.DateTime, default=datetime.utcnow)
    visible = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Post {self.titulo}>'